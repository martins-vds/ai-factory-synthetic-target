import pytest
from playwright.sync_api import sync_playwright


@pytest.mark.django_db
def test_admin_login_page_renders_in_browser(live_server):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page()
            response = page.goto(f'{live_server.url}/admin/login/')
            assert response is not None
            assert response.status == 200
            assert page.locator('input[name="username"]').is_visible()
        finally:
            browser.close()
