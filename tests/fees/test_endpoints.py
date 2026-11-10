import json
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from src.fees.gateway import HttpPaymentGateway
from src.fees.services import PaymentGatewayFailure

HTTP_GOLDEN_PATH = (
    Path(__file__).resolve().parents[2] / '.migration/characterization/source/goldens/http.json'
)
GATEWAY_GOLDEN_PATH = (
    Path(__file__).resolve().parents[2] / '.migration/characterization/source/goldens/gateway.json'
)
HTTP_GOLDENS = json.loads(
    (
        HTTP_GOLDEN_PATH
        if HTTP_GOLDEN_PATH.exists()
        else Path(__file__).parent / 'fixtures/http.json'
    ).read_text(encoding='utf-8')
)
GATEWAY_GOLDENS = json.loads(
    (
        GATEWAY_GOLDEN_PATH
        if GATEWAY_GOLDEN_PATH.exists()
        else Path(__file__).parent / 'fixtures/gateway.json'
    ).read_text(encoding='utf-8')
)


@pytest.mark.parametrize(
    ('method', 'path', 'status'),
    [
        ('get', '/fees/L3', 200),
        ('post', '/fees/L3', 405),
        ('get', '/payments/L1', 405),
        ('post', '/payments/L1', 200),
        ('get', '/ui/fees/L3/', 200),
        ('post', '/ui/fees/L3/', 405),
        ('get', '/ui/payments/L1/', 405),
        ('post', '/ui/payments/L1/', 200),
    ],
)
@pytest.mark.django_db
def test_fee_routes_allow_only_their_configured_http_method(
    client, payment_gateway, method, path, status
):
    response = getattr(client, method)(path)

    assert response.status_code == status


@pytest.mark.django_db
def test_fee_endpoint_matches_characterized_html(client):
    expected = HTTP_GOLDENS['GET /fees/{id}']['response']

    response = client.get('/fees/L3')

    assert response.status_code == expected['status']
    assert response['Content-Type'] == expected['content_type']
    assert response.content.decode() == expected['body']


@pytest.mark.django_db
def test_fee_endpoint_returns_characterized_not_found_response(client):
    response = client.get('/fees/unknown')

    assert response.status_code == 404
    assert response['Content-Type'] == 'text/html'
    assert response.content.decode() == '<p>No such loan.</p>'


@pytest.mark.django_db
def test_payment_endpoint_forwards_the_characterized_gateway_request(client, payment_gateway):
    expected = GATEWAY_GOLDENS['responses']['POST /payments/L1 via test gateway']['response']

    response = client.post('/payments/L1')

    assert response.status_code == expected['status']
    assert response['Content-Type'] == expected['content_type']
    assert response.content.decode() == expected['body']
    assert payment_gateway.requests == [('POST', '/charge?loan=L1', b'')]


@pytest.mark.django_db
def test_payment_endpoint_maps_gateway_failure_to_bad_gateway(client, payment_gateway):
    payment_gateway.status = 503
    payment_gateway.body = b'declined\n'
    expected = GATEWAY_GOLDENS['responses']['POST /payments/L2 via test gateway']['response']

    response = client.post('/payments/L1')

    assert response.status_code == expected['status']
    assert response['Content-Type'] == expected['content_type']
    assert response.content.decode() == expected['body']
    assert payment_gateway.requests == [('POST', '/charge?loan=L1', b'')]


@pytest.mark.django_db
def test_payment_endpoint_does_not_follow_gateway_redirects(client, payment_gateway):
    payment_gateway.status = 302
    payment_gateway.body = b'redirected\n'
    payment_gateway.headers = {'Location': '/other'}

    response = client.post('/payments/L1')

    assert response.status_code == 502
    assert response.content == b'redirected\n'
    assert payment_gateway.requests == [('POST', '/charge?loan=L1', b'')]


@pytest.mark.django_db
def test_payment_endpoint_rejects_unknown_loan_without_calling_gateway(client, payment_gateway):
    expected = GATEWAY_GOLDENS['responses']['POST /payments/unknown via test gateway']['response']

    response = client.post('/payments/unknown')

    assert response.status_code == expected['status']
    assert response['Content-Type'] == expected['content_type']
    assert response.content.decode() == expected['body']
    assert payment_gateway.requests == []


@pytest.mark.django_db
def test_fee_page_shows_late_fee_and_posts_payment_to_ui_route(client):
    response = client.get('/ui/fees/L3/')

    assert response.status_code == 200
    assert b'Late fee for L3' in response.content
    assert b'2025-12-15' in response.content
    assert b'19 day(s) late' in response.content
    assert b'Fee: $4.75' in response.content
    assert b'hx-post="/ui/payments/L3/"' in response.content


@pytest.mark.django_db
def test_fee_page_payment_returns_gateway_status_fragment(client, payment_gateway):
    response = client.post('/ui/payments/L1/', HTTP_HX_REQUEST='true')

    assert response.status_code == 200
    assert b'role="status"' in response.content
    assert b'charged' in response.content
    assert b'id="payment-status"' in response.content
    assert payment_gateway.requests == [('POST', '/charge?loan=L1', b'')]


@pytest.mark.django_db
def test_fee_page_payment_shows_gateway_failure_fragment(client, payment_gateway):
    payment_gateway.status = 503
    payment_gateway.body = b'declined\n'

    response = client.post('/ui/payments/L1/', HTTP_HX_REQUEST='true')

    assert response.status_code == 502
    assert b'role="alert"' in response.content
    assert b'declined' in response.content


def test_interrupted_gateway_call_is_preserved_as_the_gateway_failure_cause(monkeypatch):
    def interrupt(_request):
        raise InterruptedError('request interrupted')

    monkeypatch.setattr('src.fees.gateway._open', interrupt)

    with pytest.raises(PaymentGatewayFailure) as failure:
        HttpPaymentGateway().charge('L1')

    assert failure.value.body == 'payment gateway unavailable\n'
    assert isinstance(failure.value.__cause__, InterruptedError)


@pytest.mark.django_db
def test_interrupted_payment_request_returns_gateway_failure(monkeypatch, client):
    def interrupt(_request):
        raise InterruptedError('request interrupted')

    monkeypatch.setattr('src.fees.gateway._open', interrupt)

    response = client.post('/payments/L1')

    assert response.status_code == 502
    assert response.content == b'payment gateway unavailable\n'


@pytest.mark.django_db
def test_io_failure_returns_gateway_failure(monkeypatch, client):
    def unavailable(_request):
        raise OSError('gateway unreachable')

    monkeypatch.setattr('src.fees.gateway._open', unavailable)

    response = client.post('/payments/L1')

    assert response.status_code == 502
    assert response.content == b'payment gateway unavailable\n'


@pytest.mark.django_db(transaction=True, serialized_rollback=True)
@pytest.mark.usefixtures('restore_seed_loans_after_fee_browser_test')
def test_real_browser_can_pay_a_late_fee(live_server, payment_gateway):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page()
            page.goto(f'{live_server.url}/ui/fees/L3/')
            page.get_by_role('button', name='Pay late fee').click()

            status = page.get_by_role('status')
            status.wait_for()
            assert status.inner_text().strip() == 'charged'
            assert payment_gateway.requests == [('POST', '/charge?loan=L3', b'')]
        finally:
            browser.close()
