import pytest
from playwright.sync_api import sync_playwright


@pytest.mark.django_db
def test_loan_catalog_renders_in_browser_and_admin_is_removed(client, live_server):
    assert client.get('/admin/login/').status_code == 404

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page()
            response = page.goto(f'{live_server.url}/ui/loans/')
            assert response is not None
            assert response.status == 200
            assert page.get_by_role('heading', name='Books in good company.').is_visible()
            assert page.get_by_text('ana · ISBN 9780134685991').is_visible()
        finally:
            browser.close()
