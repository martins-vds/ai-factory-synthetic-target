import pytest


@pytest.mark.django_db
def test_seed_loans_remain_available_after_fee_browser_test(client):
    response = client.get('/loans')

    assert response.status_code == 200
    assert [line.split(';', 1)[0] for line in response.content.decode().splitlines()] == [
        'L1',
        'L2',
        'L3',
    ]
