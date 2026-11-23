import json
from pathlib import Path

import pytest
from playwright.sync_api import expect, sync_playwright

HTTP_GOLDEN_PATH = (
    Path(__file__).resolve().parents[2] / '.migration/characterization/source/goldens/http.json'
)
HTTP_FIXTURE_PATH = Path(__file__).parent / 'fixtures/http.json'
HTTP_GOLDENS = json.loads(
    (HTTP_GOLDEN_PATH if HTTP_GOLDEN_PATH.exists() else HTTP_FIXTURE_PATH).read_text(
        encoding='utf-8'
    )
)


def test_about_endpoint_matches_characterized_response(client):
    response = client.get('/about')
    expected = HTTP_GOLDENS['GET /about']['response']

    assert response.status_code == expected['status']
    assert response['Content-Type'] == expected['content_type']
    assert response.content.decode() == expected['body']


def test_about_routes_reject_non_get_requests(client):
    assert client.post('/about').status_code == 405
    assert client.post('/ui/about/').status_code == 405


@pytest.mark.django_db
def test_modern_about_page_shows_library_information_in_browser(live_server):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page()
            response = page.goto(f'{live_server.url}/ui/about/')

            assert response is not None
            assert response.status == 200
            expect(page.get_by_role('heading', name='About the Lending Library')).to_be_visible()
            expect(
                page.get_by_text(
                    'A neighborhood collection, kept in motion by the people who read it.'
                )
            ).to_be_visible()
            expect(page.get_by_text('Open Monday to Saturday, 9:00 to 18:00.')).to_be_visible()
            expect(page.get_by_text('Books are lent for 14 days.')).to_be_visible()
            expect(
                page.get_by_role('link', name='desk@lending-library.invalid')
            ).to_have_attribute('href', 'mailto:desk@lending-library.invalid')
            expect(page.get_by_role('link', name='Loans')).to_have_attribute(
                'href', '/ui/loans/'
            )
        finally:
            browser.close()
