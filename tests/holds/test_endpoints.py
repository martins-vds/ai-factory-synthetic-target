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


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('payload', 'status', 'body'),
    [
        ({}, 400, 'member and isbn are required\n'),
        (
            {'member': 'dee', 'isbn': '9780596007126'},
            409,
            'book is available\n',
        ),
        (
            {'member': 'ana', 'isbn': '9780134685991'},
            409,
            'member has this book\n',
        ),
    ],
)
def test_placement_endpoint_renders_policy_failures(client, payload, status, body):
    response = client.post('/holds', payload)

    assert response.status_code == status
    assert response['Content-Type'] == 'text/plain'
    assert response.content.decode() == body


@pytest.mark.django_db
def test_placement_endpoint_renders_duplicate_hold_failure(client):
    Hold.objects.create(
        id='H2',
        sequence=2,
        member='dee',
        isbn='9780134685991',
        placed_on=timezone.localdate(),
    )

    response = client.post('/holds', {'member': 'dee', 'isbn': '9780134685991'})

    assert response.status_code == 409
    assert response.content == b'already on hold\n'
    assert response['Content-Type'] == 'text/plain'


@pytest.mark.django_db
def test_placement_endpoint_renders_active_hold_limit_failure(client):
    today = timezone.localdate()
    Hold.objects.bulk_create(
        [
            Hold(
                id=f'H{sequence}',
                sequence=sequence,
                member='dee',
                isbn=f'other-{sequence}',
                placed_on=today,
            )
            for sequence in range(2, 6)
        ]
    )

    response = client.post('/holds', {'member': 'dee', 'isbn': '9780134685991'})

    assert response.status_code == 409
    assert response.content == b'hold limit reached\n'
    assert response['Content-Type'] == 'text/plain'


@pytest.mark.django_db
def test_cancel_endpoint_renders_unknown_and_already_cancelled_failures(client):
    unknown = client.post('/holds/unknown/cancel')
    Hold.objects.create(
        id='H2',
        sequence=2,
        member='dee',
        isbn='9780134685991',
        placed_on=timezone.localdate(),
        cancelled_on=timezone.localdate(),
    )
    cancelled = client.post('/holds/H2/cancel')

    assert unknown.status_code == 404
    assert unknown.content == b'no such hold\n'
    assert cancelled.status_code == 409
    assert cancelled.content == b'hold already cancelled\n'
    assert unknown['Content-Type'] == cancelled['Content-Type'] == 'text/plain'


@pytest.mark.django_db
def test_hold_write_routes_reject_unsupported_methods(client):
    assert client.put('/holds').status_code == 405
    assert client.get('/holds/H1/cancel').status_code == 405
