from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import date
from threading import Barrier, local

import pytest
from django.db import connections

from src.holds.models import Hold
from src.holds.repository import DjangoHoldRepository
from src.holds.services import (
    HoldApplication,
    HoldFailure,
    HoldFailureCode,
    HoldIdentity,
)


class ConcurrentPlacementRepository(DjangoHoldRepository):
    def __init__(self):
        self.ready = Barrier(2)
        self.state = local()

    @contextmanager
    def placement(self):
        self.ready.wait(timeout=5)
        with super().placement():
            self.state.in_placement = True
            try:
                yield
            finally:
                self.state.in_placement = False

    def active_count_for_member(self, member, today):
        assert self.state.in_placement
        return super().active_count_for_member(member, today)

    def next_identity(self):
        assert self.state.in_placement
        return super().next_identity()

    def create(self, **kwargs):
        assert self.state.in_placement
        return super().create(**kwargs)


class FixedClock:
    def today(self):
        return date(2026, 11, 23)


class LoanStateLookup:
    def active_loan_for_isbn(self, isbn):
        return type('LoanState', (), {'borrower': 'ana'})()


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


@pytest.mark.django_db(transaction=True)
def test_concurrent_placements_cannot_exceed_member_limit_or_reuse_ids():
    Hold.objects.all().delete()
    today = date(2026, 11, 23)
    for sequence in range(1, 4):
        Hold.objects.create(
            id=f'H{sequence}',
            sequence=sequence,
            member='dee',
            isbn=f'existing-{sequence}',
            placed_on=today,
        )
    repository = ConcurrentPlacementRepository()

    def place(isbn):
        connections.close_all()
        try:
            return HoldApplication(repository, FixedClock(), LoanStateLookup()).place('dee', isbn)
        finally:
            connections.close_all()

    with ThreadPoolExecutor(max_workers=2) as workers:
        results = list(workers.map(place, ['first', 'second']))

    assert results.count(HoldFailure(HoldFailureCode.HOLD_LIMIT)) == 1
    assert sum(not isinstance(result, HoldFailure) for result in results) == 1
    assert Hold.objects.filter(member='dee', cancelled_on__isnull=True).count() == 4
    assert Hold.objects.filter(id='H4', member='dee').exists()
