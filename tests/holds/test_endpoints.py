from datetime import date, timedelta

import pytest
from django.utils import timezone

from src.holds.models import Hold


@pytest.mark.django_db
def test_seeded_hold_matches_the_characterized_record():
    hold = Hold.objects.get(pk='H1')

    assert (hold.sequence, hold.member, hold.isbn) == (1, 'bo', '9780134685991')
    assert hold.placed_on == date(2026, 1, 5)
    assert hold.expires_on == date(2026, 2, 4)
    assert hold.cancelled_on is None


@pytest.mark.django_db
def test_placement_persists_a_hold_for_later_listing(client):
    today = timezone.localdate()
    response = client.post(
        '/holds',
        {'member': 'dee', 'isbn': '9780134685991'},
    )

    assert response.status_code == 201
    assert response['Content-Type'] == 'text/plain'
    assert response.content.decode() == (
        f'H2;dee;9780134685991;{today.isoformat()};{(today + timedelta(days=30)).isoformat()}\n'
    )
    assert Hold.objects.get(pk='H2').placed_on == today

    listing = client.get('/holds')

    assert listing.status_code == 200
    assert listing.content.decode() == response.content.decode()


@pytest.mark.django_db
def test_cancel_endpoint_records_the_date_and_removes_hold_from_active_list(client):
    response = client.post('/holds', {'member': 'dee', 'isbn': '9780134685991'})
    placed = response.content.decode()
    today = timezone.localdate()

    cancelled = client.post('/holds/H2/cancel')

    assert cancelled.status_code == 200
    assert cancelled.content.decode() == placed
    assert Hold.objects.get(pk='H2').cancelled_on == today
    assert client.get('/holds').content == b'\n'
