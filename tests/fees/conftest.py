import importlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

import pytest


@pytest.fixture(scope='module')
def restore_seed_loans_after_fee_browser_test(django_db_blocker):
    yield
    with django_db_blocker.unblock():
        from django.apps import apps
        from django.db import connection

        apps.get_model('loans', 'Loan').objects.all().delete()
        seed_loans = importlib.import_module('src.loans.migrations.0001_initial').seed_loans
        with connection.schema_editor() as schema_editor:
            seed_loans(apps, schema_editor)


@pytest.fixture
def payment_gateway(monkeypatch):
    class State:
        def __init__(self):
            self.status = 200
            self.body = b'charged\n'
            self.requests = []
            self.headers = {}

    state = State()

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            state.requests.append(
                (
                    self.command,
                    self.path,
                    self.rfile.read(int(self.headers.get('Content-Length', 0))),
                )
            )
            self.send_response(state.status)
            for name, value in state.headers.items():
                self.send_header(name, value)
            self.end_headers()
            self.wfile.write(state.body)

        def log_message(self, format, *args):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    monkeypatch.setenv('PAYMENT_GATEWAY_URL', f'http://127.0.0.1:{server.server_port}')
    try:
        yield state
    finally:
        server.shutdown()
        thread.join()
        server.server_close()
