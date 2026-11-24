from datetime import date

import pytest

from src.holds.models import Hold
from src.holds.repository import DjangoHoldRepository
from src.holds.services import HoldIdentity


@pytest.mark.django_db
def test_repository_filters_active_holds_by_expiry_cancellation_and_isbn():
    today = date(2026, 11, 23)
    Hold.objects.create(
        id='H3',
        sequence=3,
        member='dee',
        isbn='123',
        placed_on=today,
        cancelled_on=today,
    )
    Hold.objects.create(
        id='H4',
        sequence=4,
        member='eli',
        isbn='123',
        placed_on=date(2026, 10, 24),
    )
    Hold.objects.create(
        id='H5',
        sequence=5,
        member='ana',
        isbn='456',
        placed_on=today,
    )
    Hold.objects.create(
        id='H6',
        sequence=6,
        member='bo',
        isbn='123',
        placed_on=date(2026, 10, 23),
    )
    repository = DjangoHoldRepository()

    assert [hold.id for hold in repository.active(None, today)] == ['H4', 'H5']
    assert [hold.id for hold in repository.active('123', today)] == ['H4']
    assert repository.active_count_for_member('eli', today) == 1
    assert repository.has_active_for_member_and_isbn('eli', '123', today)
    assert repository.next_identity().id == 'H7'


@pytest.mark.django_db
def test_repository_starts_identifier_sequence_at_one_when_empty():
    Hold.objects.all().delete()

    assert DjangoHoldRepository().next_identity() == HoldIdentity('H1', 1)


@pytest.mark.django_db(transaction=True)
def test_repository_cancellation_is_atomic():
    Hold.objects.create(
        id='H2',
        sequence=2,
        member='dee',
        isbn='123',
        placed_on=date(2026, 11, 23),
    )

    cancelled = DjangoHoldRepository().cancel('H2', date(2026, 11, 24))

    assert cancelled.cancelled_on == date(2026, 11, 24)
