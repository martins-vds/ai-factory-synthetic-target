import argparse
import difflib
import json
import os
import re
import shutil
import socket
import subprocess
import tempfile
import threading
import time
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib import error, parse, request

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'legacy'
GRAPH = ROOT / '.migration/graphs/source/full/knowledge-graph.json'
GOLDENS = ROOT / '.migration/characterization/source/goldens'
CASES = (
    ('GET /about', 'GET', '/about', None),
    ('POST /payments/{id}', 'POST', '/payments/L3', None),
    ('GET /fees/{id}', 'GET', '/fees/L3', None),
    ('GET /loans', 'GET', '/loans', None),
    ('GET /loans/{id}', 'GET', '/loans/L1', None),
    ('POST /loans', 'POST', '/loans', {'member': 'dee', 'isbn': '123'}),
    ('GET /holds', 'GET', '/holds', None),
    ('POST /holds', 'POST', '/holds', {'member': 'dee', 'isbn': '9780134685991'}),
    ('POST /holds/{id}/cancel', 'POST', '/holds/H2/cancel', None),
    ('POST /loans/{id}/return', 'POST', '/loans/L1/return', None),
)
EDGE_CASES = (
    ('GET /fees/L1 before return', 'GET', '/fees/L1', None),
    ('GET /fees/L2 early return', 'GET', '/fees/L2', None),
    ('GET /loans/unknown', 'GET', '/loans/unknown', None),
    ('GET /fees/unknown', 'GET', '/fees/unknown', None),
    ('POST /loans/missing-member', 'POST', '/loans', {'isbn': '456'}),
    ('POST /loans/missing-isbn', 'POST', '/loans', {'member': 'dee'}),
    ('POST /loans/blank-fields', 'POST', '/loans', {'member': '', 'isbn': ''}),
    ('POST /loans/delimiter-fields', 'POST', '/loans', {'member': 'a;b', 'isbn': '123;456'}),
    ('GET /loans/L5', 'GET', '/loans/L5', None),
    ('POST /loans/L2/return again', 'POST', '/loans/L2/return', None),
    ('POST /payments/unknown', 'POST', '/payments/unknown', None),
    ('GET /loans after writes', 'GET', '/loans', None),
    ('POST /holds/missing-member', 'POST', '/holds', {'isbn': '9780134685991'}),
    ('POST /holds/missing-isbn', 'POST', '/holds', {'member': 'dee'}),
    ('POST /holds/blank-fields', 'POST', '/holds', {'member': ' ', 'isbn': ''}),
    ('POST /holds/book-available', 'POST', '/holds', {'member': 'dee', 'isbn': '9780596007126'}),
    ('POST /holds/borrower', 'POST', '/holds', {'member': 'ana', 'isbn': '9780134685991'}),
    ('POST /holds/duplicate setup', 'POST', '/holds', {'member': 'dee', 'isbn': '9780134685991'}),
    ('POST /holds/duplicate', 'POST', '/holds', {'member': 'dee', 'isbn': '9780134685991'}),
    ('POST /holds/second member', 'POST', '/holds', {'member': 'eli', 'isbn': '9780134685991'}),
    ('GET /holds after writes', 'GET', '/holds', None),
    ('GET /holds filtered', 'GET', '/holds?isbn=9780134685991', None),
    ('GET /holds filtered empty', 'GET', '/holds?isbn=', None),
    ('POST /holds/unknown cancel', 'POST', '/holds/unknown/cancel', None),
    ('POST /holds/already cancelled', 'POST', '/holds/H2/cancel', None),
    ('POST /holds/cancel expired seed', 'POST', '/holds/H1/cancel', None),
    ('POST /holds/cancel expired seed again', 'POST', '/holds/H1/cancel', None),
)


def verify_graph_coverage():
    graph = json.loads(GRAPH.read_text(encoding='utf-8'))
    endpoints = {node['name'] for node in graph['nodes'] if node.get('type') == 'endpoint'}
    covered = {case[0] for case in CASES}
    if endpoints != covered:
        missing = sorted(endpoints - covered)
        unexpected = sorted(covered - endpoints)
        raise RuntimeError(f'graph endpoint mismatch; missing={missing}, unexpected={unexpected}')


def get_response(method, path, form, base_url):
    body = parse.urlencode(form).encode() if form is not None else None
    headers = {'Content-Type': 'application/x-www-form-urlencoded'} if body is not None else {}
    req = request.Request(f'{base_url}{path}', data=body, headers=headers, method=method)
    try:
        response = request.urlopen(req, timeout=10)
    except error.HTTPError as exc:
        response = exc
    with response:
        return {
            'status': response.status,
            'content_type': response.headers.get('Content-Type'),
            'body': response.read().decode('utf-8'),
        }


def wait_until_ready(process, output, base_url):
    deadline = time.monotonic() + 180
    while time.monotonic() < deadline:
        if process.poll() is not None:
            output.seek(0)
            raise RuntimeError(
                f'legacy app exited early:\n{output.read().decode(errors="replace")[-4000:]}'
            )
        try:
            with request.urlopen(f'{base_url}/about', timeout=1) as response:
                if response.status == 200:
                    return
        except (OSError, error.URLError):
            time.sleep(0.5)
    raise TimeoutError(f'legacy app did not become ready at {base_url}')


def get_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def run_source(source_dir, env, exercise, port=None, seed_sql=None):
    base_url = f'http://127.0.0.1:{port or 8080}'
    process_env = os.environ.copy()
    process_env.pop('PORT', None)
    process_env.pop('PAYMENT_GATEWAY_URL', None)
    process_env.update(env)
    if port is not None:
        process_env['PORT'] = str(port)
    seed_path = source_dir / 'src/main/resources/META-INF/seed.sql'
    original_seed = seed_path.read_bytes() if seed_sql is not None else None
    try:
        if seed_sql is not None:
            seed_path.write_text(seed_sql, encoding='utf-8')
        with tempfile.TemporaryFile() as output:
            process = subprocess.Popen(
                ['bash', str(source_dir / 'run.sh')],
                cwd=source_dir,
                env=process_env,
                stdout=output,
                stderr=subprocess.STDOUT,
            )
            try:
                wait_until_ready(process, output, base_url)
                return exercise(base_url)
            finally:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
    finally:
        if original_seed is not None:
            seed_path.write_bytes(original_seed)


def exercise_http(base_url):
    observations = {}
    edge_cases = {}
    for endpoint, method, path, form in CASES[:-1]:
        observations[endpoint] = {
            'request': {
                'method': method,
                'path': path,
                'form': form,
            },
            'response': get_response(method, path, form, base_url),
        }
    for name, method, path, form in EDGE_CASES:
        edge_cases[name] = {
            'request': {
                'method': method,
                'path': path,
                'form': form,
            },
            'response': get_response(method, path, form, base_url),
        }
    endpoint, method, path, form = CASES[-1]
    observations[endpoint] = {
        'request': {'method': method, 'path': path, 'form': form},
        'response': get_response(method, path, form, base_url),
    }
    return observations, edge_cases


def exercise_browser(base_url):
    pages = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page()
            for path in ('/about', '/fees/L3'):
                response = page.goto(f'{base_url}{path}', wait_until='domcontentloaded')
                if response is None:
                    raise RuntimeError(f'browser navigation returned no response for {path}')
                pages.append(
                    {
                        'path': path,
                        'status': response.status,
                        'heading': page.locator('h1').inner_text(),
                    }
                )
        finally:
            browser.close()
    return {'pages': pages}


def normalize(observation, endpoint):
    response = observation['response']
    body = re.sub(r'\d{4}-\d{2}-\d{2}', '<date>', response['body'])
    if endpoint.startswith('GET /fees/'):
        body = re.sub(r'\d+ day\(s\) late', '<days> day(s) late', body)
        body = re.sub(r'Fee: \$\d+\.\d{2}', 'Fee: $<amount>', body)
    return {
        'request': observation['request'],
        'response': {
            'status': response['status'],
            'content_type': response['content_type'],
            'body': body,
        },
    }


def write_or_compare(name, observation, record):
    path = GOLDENS / f'{name}.json'
    if record:
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
        merged = {**observation, **{key: value for key, value in existing.items()}}
        path.write_text(json.dumps(merged, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        return
    rendered = json.dumps(observation, indent=2, sort_keys=True) + '\n'
    expected = json.loads(path.read_text(encoding='utf-8'))
    if name in ('http', 'edge-cases', 'hold-listing', 'hold-expired', 'hold-limit'):
        actual = {key: normalize(value, key) for key, value in observation.items()}
        baseline = {key: normalize(value, key) for key, value in expected.items()}
    else:
        actual = observation
        baseline = expected
    if actual != baseline:
        before = json.dumps(baseline, indent=2, sort_keys=True).splitlines()
        after = json.dumps(actual, indent=2, sort_keys=True).splitlines()
        diff = '\n'.join(difflib.unified_diff(before, after, fromfile=str(path), tofile='observed'))
        raise AssertionError(f'golden mismatch:\n{diff}')


def make_gateway():
    requests = []

    class GatewayHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            requests.append(
                {
                    'method': self.command,
                    'path': self.path,
                    'body': self.rfile.read(int(self.headers.get('Content-Length', 0))).decode(),
                }
            )
            status, body = (200, 'charged\n') if 'loan=L1' in self.path else (503, 'declined\n')
            self.send_response(status)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(body.encode())

        def log_message(self, format, *args):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), GatewayHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, requests


def exercise_gateway(base_url, requests):
    observations = {}
    for loan_id in ('L1', 'L2', 'unknown'):
        name = f'POST /payments/{loan_id} via test gateway'
        observations[name] = {
            'request': {'method': 'POST', 'path': f'/payments/{loan_id}', 'form': None},
            'response': get_response('POST', f'/payments/{loan_id}', None, base_url),
        }
    return {'responses': observations, 'gateway_requests': requests}


def exercise_default(base_url):
    http, edge_cases = exercise_http(base_url)
    browser = exercise_browser(base_url)
    return http, edge_cases, browser


def source_seed():
    return (SOURCE / 'src/main/resources/META-INF/seed.sql').read_text(encoding='utf-8')


def hold_seed_for_date(days_ago):
    placed_on = date.today() - timedelta(days=days_ago)
    return source_seed().replace("DATE '2026-01-05'", f"DATE '{placed_on}'", 1)


def exercise_hold_listing(base_url):
    observations = {
        'GET /holds on expiry date': observe('GET', '/holds', None, base_url),
    }
    observations['POST /holds first isbn'] = observe(
        'POST', '/holds', {'member': 'dee', 'isbn': '9780134685991'}, base_url
    )
    observations['POST /holds second isbn'] = observe(
        'POST', '/holds', {'member': 'eli', 'isbn': '9781111111111'}, base_url
    )
    observations['GET /holds ordered'] = observe('GET', '/holds', None, base_url)
    observations['GET /holds filtered second isbn'] = observe(
        'GET', '/holds?isbn=9781111111111', None, base_url
    )
    observations['GET /holds filtered unknown isbn'] = observe(
        'GET', '/holds?isbn=unknown', None, base_url
    )
    return observations


def observe(method, path, form, base_url):
    return {
        'request': {'method': method, 'path': path, 'form': form},
        'response': get_response(method, path, form, base_url),
    }


def hold_listing_seed():
    today = date.today()
    return hold_seed_for_date(30) + (
        "\nINSERT INTO LOAN (ID, MEMBER, ISBN, LENT_ON, RETURNED_ON) "
        f"VALUES ('L4', 'cy', '9781111111111', DATE '{today}', NULL);\n"
    )


def exercise_hold_expired(base_url):
    return {'GET /holds one day after expiry': observe('GET', '/holds', None, base_url)}


def hold_limit_seed():
    today = date.today()
    seed = hold_seed_for_date(0)
    extra_loans = (
        ('L4', '9781111111111'),
        ('L5', '9782222222222'),
        ('L6', '9783333333333'),
        ('L7', '9784444444444'),
    )
    for loan_id, isbn in extra_loans:
        seed += (
            f"\nINSERT INTO LOAN (ID, MEMBER, ISBN, LENT_ON, RETURNED_ON) "
            f"VALUES ('{loan_id}', 'cy', '{isbn}', DATE '{today}', NULL);\n"
        )
    for hold_id, seq, isbn in (
        ('H2', 2, '9780134685991'),
        ('H3', 3, '9781111111111'),
        ('H4', 4, '9782222222222'),
    ):
        seed += (
            f"INSERT INTO HOLD (ID, SEQ, MEMBER, ISBN, PLACED_ON, CANCELLED_ON) "
            f"VALUES ('{hold_id}', {seq}, 'dee', '{isbn}', DATE '{today}', NULL);\n"
        )
    return seed


def exercise_hold_limit(base_url):
    return {
        'POST /holds with three active holds': observe(
            'POST', '/holds', {'member': 'dee', 'isbn': '9783333333333'}, base_url
        ),
        'POST /holds with four active holds': observe(
            'POST', '/holds', {'member': 'dee', 'isbn': '9784444444444'}, base_url
        ),
    }


def send_setup_requests(base_url, requests):
    for method, path, form, expected_status in requests:
        response = get_response(method, path, form, base_url)
        if response['status'] != expected_status:
            raise AssertionError(
                f'setup {method} {path} returned {response["status"]}, expected {expected_status}'
            )


def exercise_borrower_and_duplicate(base_url):
    send_setup_requests(
        base_url,
        [
            ('POST', '/loans/L1/return', None, 200),
            ('POST', '/loans', {'member': 'cy', 'isbn': '9780134685991'}, 201),
            ('POST', '/holds', {'member': 'ana', 'isbn': '9780134685991'}, 201),
            ('POST', '/loans/L4/return', None, 200),
            ('POST', '/loans', {'member': 'ana', 'isbn': '9780134685991'}, 201),
        ],
    )
    return {
        'POST /holds borrower and duplicate': observe(
            'POST', '/holds', {'member': 'ana', 'isbn': '9780134685991'}, base_url
        )
    }


def exercise_four_active_holds(base_url):
    for isbn in (
        '9780134685991',
        '9781111111111',
        '9782222222222',
        '9783333333333',
    ):
        if isbn != '9780134685991':
            send_setup_requests(base_url, [('POST', '/loans', {'member': 'cy', 'isbn': isbn}, 201)])
        send_setup_requests(base_url, [('POST', '/holds', {'member': 'dee', 'isbn': isbn}, 201)])


def exercise_duplicate_and_limit(base_url):
    exercise_four_active_holds(base_url)
    return {
        'POST /holds duplicate and limit': observe(
            'POST', '/holds', {'member': 'dee', 'isbn': '9780134685991'}, base_url
        )
    }


def exercise_available_and_limit(base_url):
    exercise_four_active_holds(base_url)
    return {
        'POST /holds available and limit': observe(
            'POST', '/holds', {'member': 'dee', 'isbn': '9780596007126'}, base_url
        )
    }


def assert_hold_precedence(observations):
    expected = {
        'POST /holds borrower and duplicate': (409, 'member has this book\n'),
        'POST /holds duplicate and limit': (409, 'already on hold\n'),
        'POST /holds available and limit': (409, 'book is available\n'),
    }
    for name, (status, body) in expected.items():
        response = observations[name]['response']
        if response['status'] != status or response['body'] != body:
            raise AssertionError(f'{name} returned {response!r}, expected {(status, body)!r}')


def assert_hold_predictions(edge_cases, listing, expired, limit):
    expected_statuses = {
        'POST /holds/missing-member': 400,
        'POST /holds/missing-isbn': 400,
        'POST /holds/blank-fields': 400,
        'POST /holds/book-available': 409,
        'POST /holds/borrower': 409,
        'POST /holds/duplicate setup': 201,
        'POST /holds/duplicate': 409,
        'POST /holds/second member': 201,
        'POST /holds/unknown cancel': 404,
        'POST /holds/already cancelled': 409,
        'POST /holds/cancel expired seed': 200,
        'POST /holds/cancel expired seed again': 409,
    }
    for name, status in expected_statuses.items():
        observed = edge_cases[name]['response']['status']
        if observed != status:
            raise AssertionError(f'{name} returned {observed}, expected {status}')

    empty = edge_cases['GET /holds filtered empty']['response']['body']
    if empty != '\n':
        raise AssertionError(f'empty hold listing was {empty!r}, expected a newline')
    ordered = edge_cases['GET /holds after writes']['response']['body'].splitlines()
    if [row.split(';', 1)[0] for row in ordered] != ['H3', 'H4']:
        raise AssertionError(f'active holds were not returned in sequence order: {ordered!r}')
    if edge_cases['GET /holds filtered']['response']['body'] != '\n'.join(ordered) + '\n':
        raise AssertionError('ISBN-filtered hold listing did not return matching holds')
    unavailable = edge_cases['POST /holds/book-available']['response']['body']
    if unavailable != 'book is available\n':
        raise AssertionError(f'unavailable-book response was {unavailable!r}')
    seeded = edge_cases['POST /holds/cancel expired seed']['response']['body']
    if seeded != 'H1;bo;9780134685991;2026-01-05;2026-02-04\n':
        raise AssertionError(f'seeded hold was {seeded!r}')

    today = date.today().isoformat()
    boundary = listing['GET /holds on expiry date']['response']['body']
    expected_boundary = f'H1;bo;9780134685991;{(date.today() - timedelta(days=30)).isoformat()};{today}\n'
    if boundary != expected_boundary:
        raise AssertionError(f'hold was not active through its expiry date: {boundary!r}')
    if listing['GET /holds ordered']['response']['body'].splitlines()[0] != expected_boundary.strip():
        raise AssertionError('hold ordering did not put the seeded sequence first')
    filtered = listing['GET /holds filtered second isbn']['response']['body']
    if not filtered.startswith('H3;eli;9781111111111;'):
        raise AssertionError(f'ISBN filter returned {filtered!r}')
    if listing['GET /holds filtered unknown isbn']['response']['body'] != '\n':
        raise AssertionError('unknown ISBN did not produce an empty newline-terminated listing')
    if expired['GET /holds one day after expiry']['response']['body'] != '\n':
        raise AssertionError('expired hold remained active after its expiry date')

    accepted = limit['POST /holds with three active holds']
    rejected = limit['POST /holds with four active holds']
    if accepted['response']['status'] != 201 or not accepted['response']['body'].startswith('H5;dee;'):
        raise AssertionError(f'three active holds did not permit a fourth: {accepted!r}')
    if rejected['response']['status'] != 409 or rejected['response']['body'] != 'hold limit reached\n':
        raise AssertionError(f'four active holds did not trigger the limit: {rejected!r}')


def assert_predictions(http, edge_cases, browser, restart, payments):
    expected_statuses = {
        'GET /loans/unknown': 404,
        'GET /fees/unknown': 404,
        'POST /loans/missing-member': 400,
        'POST /loans/missing-isbn': 400,
        'POST /loans/blank-fields': 201,
        'POST /loans/delimiter-fields': 201,
        'POST /loans/L2/return again': 200,
        'POST /payments/unknown': 404,
    }
    for name, status in expected_statuses.items():
        observed = edge_cases[name]['response']['status']
        if observed != status:
            raise AssertionError(f'{name} returned {observed}, expected {status}')

    loan_fields = http['POST /loans']['response']['body'].strip().split(';')
    lent_on, due_on = date.fromisoformat(loan_fields[3]), date.fromisoformat(loan_fields[4])
    if due_on != lent_on + timedelta(days=14):
        raise AssertionError(f'loan due date {due_on} is not 14 days after {lent_on}')
    if 'Fee: $10.00' not in edge_cases['GET /fees/L1 before return']['response']['body']:
        raise AssertionError('late fee did not reach its $10.00 cap')
    if 'Fee: $0.00' not in edge_cases['GET /fees/L2 early return']['response']['body']:
        raise AssertionError('early-returned loan did not have a zero late fee')
    if 'L5;;;' not in edge_cases['POST /loans/blank-fields']['response']['body']:
        raise AssertionError('blank loan fields were not preserved')
    if 'L6;a;b;123;456;' not in edge_cases['POST /loans/delimiter-fields']['response']['body']:
        raise AssertionError('delimiter-containing fields were not emitted raw')
    if '2026-01-20' in edge_cases['POST /loans/L2/return again']['response']['body']:
        raise AssertionError('repeat return did not overwrite the previous return date')
    if [page['status'] for page in browser['pages']] != [200, 200]:
        raise AssertionError('browser pages did not load successfully')
    restarted_rows = restart['body'].strip().splitlines()
    if len(restarted_rows) != 3 or any(row.startswith('L4;') for row in restarted_rows):
        raise AssertionError('restart did not reset the in-memory database to its three seed rows')
    if payments['responses']['POST /payments/L1 via test gateway']['response']['status'] != 200:
        raise AssertionError('successful gateway response did not map to HTTP 200')
    if payments['responses']['POST /payments/L2 via test gateway']['response']['status'] != 502:
        raise AssertionError('non-200 gateway response did not map to HTTP 502')
    if len(payments['gateway_requests']) != 2:
        raise AssertionError('unknown loan unexpectedly called the payment gateway')


def main():
    parser = argparse.ArgumentParser(
        description='Characterize the pinned legacy HTTP and browser behavior.'
    )
    parser.add_argument(
        '--record', action='store_true', help='write current observations to golden files'
    )
    parser.add_argument(
        '--keep-source-copy',
        type=Path,
        help='retain the isolated built source copy at this path for coverage reporting',
    )
    parser.add_argument(
        '--hold-precedence', action='store_true', help='characterize hold refusal precedence only'
    )
    args = parser.parse_args()
    if args.hold_precedence:
        with tempfile.TemporaryDirectory() as workdir:
            source_dir = Path(workdir) / 'legacy'
            shutil.copytree(SOURCE, source_dir, ignore=shutil.ignore_patterns('target', '.git'))
            observations = {}
            for exercise in (
                exercise_borrower_and_duplicate,
                exercise_duplicate_and_limit,
                exercise_available_and_limit,
            ):
                observations.update(run_source(source_dir, {}, exercise, port=get_port()))
        assert_hold_precedence(observations)
        write_or_compare('hold-precedence', observations, args.record)
        action = 'recorded' if args.record else 'verified'
        print(f'{action} {len(observations)} hold refusal precedence exchanges')
        return

    verify_graph_coverage()
    with tempfile.TemporaryDirectory() as workdir:
        source_dir = Path(workdir) / 'legacy'
        shutil.copytree(SOURCE, source_dir, ignore=shutil.ignore_patterns('target', '.git'))
        http, edge_cases, browser = run_source(source_dir, {}, exercise_default)
        hold_listing = run_source(
            source_dir,
            {},
            exercise_hold_listing,
            port=get_port(),
            seed_sql=hold_listing_seed(),
        )
        hold_expired = run_source(
            source_dir,
            {},
            exercise_hold_expired,
            port=get_port(),
            seed_sql=hold_seed_for_date(31),
        )
        hold_limit = run_source(
            source_dir, {}, exercise_hold_limit, port=get_port(), seed_sql=hold_limit_seed()
        )
        restart = run_source(
            source_dir,
            {},
            lambda base_url: get_response('GET', '/loans', None, base_url),
            port=get_port(),
        )
        gateway, thread, gateway_requests = make_gateway()
        try:
            gateway_url = f'http://127.0.0.1:{gateway.server_port}'
            payments = run_source(
                source_dir,
                {'PAYMENT_GATEWAY_URL': gateway_url},
                lambda base_url: exercise_gateway(base_url, gateway_requests),
                port=get_port(),
            )
        finally:
            gateway.shutdown()
            gateway.server_close()
            thread.join(timeout=5)

        if args.keep_source_copy:
            shutil.copytree(source_dir, args.keep_source_copy)

    assert_predictions(http, edge_cases, browser, restart, payments)
    assert_hold_predictions(edge_cases, hold_listing, hold_expired, hold_limit)

    write_or_compare('http', http, args.record)
    write_or_compare('edge-cases', edge_cases, args.record)
    write_or_compare('hold-listing', hold_listing, args.record)
    write_or_compare('hold-expired', hold_expired, args.record)
    write_or_compare('hold-limit', hold_limit, args.record)
    write_or_compare('browser', browser, args.record)
    write_or_compare('restart', restart, args.record)
    write_or_compare('gateway', payments, args.record)
    action = 'recorded' if args.record else 'verified'
    print(
        f'{action} {len(http)} source endpoints, {len(edge_cases)} edge cases, '
        f'{len(browser["pages"])} browser pages, {len(hold_listing) + len(hold_expired) + len(hold_limit)} '
        f'hold observations, restart reset, and gateway mappings'
    )


if __name__ == '__main__':
    main()
