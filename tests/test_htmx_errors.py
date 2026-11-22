from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

HTMX_CDN_URL = 'https://cdn.jsdelivr.net/npm/htmx.org@2.0.11/dist/htmx.min.js'
HTMX_FIXTURE = Path(__file__).parent / 'fixtures' / 'htmx-2.0.11.min.js'


@pytest.fixture
def htmx_page(live_server):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.route(
            HTMX_CDN_URL,
            lambda route: route.fulfill(
                path=str(HTMX_FIXTURE),
                content_type='application/javascript',
            ),
        )
        page.route(
            'https://cdn.jsdelivr.net/npm/daisyui@4.12.24/dist/full.min.css',
            lambda route: route.abort(),
        )
        try:
            yield page
        finally:
            browser.close()


def assert_error_fragment_swapped(
    page,
    *,
    base_url,
    page_path,
    request_path,
    button_name,
    status,
    target,
    message,
    fill_inputs=(),
):
    request = {}

    def respond_with_error(route):
        if route.request.method != 'POST':
            route.continue_()
            return

        request['headers'] = route.request.headers
        route.fulfill(
            status=status,
            content_type='text/html',
            body=f'<div id="{target}"><p role="alert">{message}</p></div>',
        )

    page.route(f'**{request_path}', respond_with_error)
    page.goto(f'{base_url}{page_path}')
    assert page.evaluate('typeof htmx') == 'object'
    assert page.evaluate(
        'htmx.config.responseHandling.map(({code, swap, error}) => [code, swap, error ?? null])'
    ) == [
        ['204', False, None],
        ['[23]..', True, None],
        ['[45]..', True, True],
        ['...', False, None],
    ]

    for selector, value in fill_inputs:
        page.locator(selector).fill(value)

    with page.expect_response(lambda response: response.url.endswith(request_path)) as response:
        page.get_by_role('button', name=button_name).click()

    assert response.value.status == status
    assert request['headers']['hx-request'] == 'true'
    assert request['headers']['hx-target'] == target
    assert page.locator(f'#{target} [role="alert"]').inner_text() == message


@pytest.mark.django_db(transaction=True)
def test_payment_error_fragment_replaces_payment_status(htmx_page, live_server):
    assert_error_fragment_swapped(
        htmx_page,
        base_url=live_server.url,
        page_path='/ui/fees/L1/',
        request_path='/ui/payments/L1/',
        button_name='Pay late fee',
        status=502,
        target='payment-status',
        message='Payment declined.',
    )


@pytest.mark.django_db(transaction=True)
def test_return_error_fragment_replaces_return_status(htmx_page, live_server):
    assert_error_fragment_swapped(
        htmx_page,
        base_url=live_server.url,
        page_path='/ui/loans/L1/',
        request_path='/ui/loans/L1/return/',
        button_name='Return book',
        status=409,
        target='return-status',
        message='This loan was already returned.',
    )


@pytest.mark.django_db(transaction=True)
def test_lending_error_fragment_replaces_loan_form(htmx_page, live_server):
    assert_error_fragment_swapped(
        htmx_page,
        base_url=live_server.url,
        page_path='/ui/loans/new/',
        request_path='/ui/loans/new/',
        button_name='Lend book',
        status=422,
        target='loan-form',
        message='The lending service is unavailable.',
        fill_inputs=(('input[name="member"]', 'reader'), ('input[name="isbn"]', '123')),
    )
