from dataclasses import dataclass
from datetime import date, timedelta

import pytest

from src.holds.services import HoldApplication, HoldError, HoldIdentity


@dataclass
class FakeHold:
    id: str
    sequence: int
    member: str
    isbn: str
    placed_on: date
    cancelled_on: date | None = None

    @property
    def expires_on(self):
        return self.placed_on + timedelta(days=30)


class FixedClock:
    def today(self):
        return date(2026, 11, 23)


class FakeLoanStateLookup:
    def __init__(self, borrowers=None):
        self.borrowers = borrowers or {}

    def active_loan_for_isbn(self, isbn):
        member = self.borrowers.get(isbn)
        return None if member is None else type('LoanState', (), {'member': member})()


class FakeHoldRepository:
    def __init__(self, holds=None):
        self.holds = list(holds or [])

    def active(self, isbn, today):
        return [
            hold
            for hold in sorted(self.holds, key=lambda record: record.sequence)
            if hold.cancelled_on is None
            and hold.expires_on >= today
            and (isbn is None or hold.isbn == isbn)
        ]

    def active_for_member(self, member, today):
        return [hold for hold in self.active(None, today) if hold.member == member]

    def active_count_for_member(self, member, today):
        return len(self.active_for_member(member, today))

    def has_active_for_member_and_isbn(self, member, isbn, today):
        return any(hold.member == member and hold.isbn == isbn for hold in self.active(None, today))

    def next_identity(self):
        sequence = max((hold.sequence for hold in self.holds), default=0) + 1
        return HoldIdentity(f'H{sequence}', sequence)

    def create(self, *, identity, member, isbn, placed_on):
        hold = FakeHold(identity.id, identity.sequence, member, isbn, placed_on)
        self.holds.append(hold)
        return hold

    def find(self, hold_id):
        return next((hold for hold in self.holds if hold.id == hold_id), None)

    def cancel(self, hold_id, cancelled_on):
        hold = self.find(hold_id)
        hold.cancelled_on = cancelled_on
        return hold


def application(holds=None, borrowers=None):
    return HoldApplication(
        FakeHoldRepository(holds),
        FixedClock(),
        FakeLoanStateLookup(borrowers),
    )


@pytest.mark.parametrize(
    ('member', 'isbn'),
    [('', '123'), (' ', '123'), ('dee', ''), ('dee', ' ')],
)
def test_placement_rejects_missing_or_blank_values(member, isbn):
    result = application(borrowers={'123': 'ana'}).place(member, isbn)

    assert result == HoldError(400, 'member and isbn are required')


def test_placement_requires_an_open_loan_and_another_borrower():
    app = application(borrowers={'borrowed': 'dee'})

    assert app.place('dee', 'available') == HoldError(409, 'book is available')
    assert app.place('dee', 'borrowed') == HoldError(409, 'member has this book')


def test_placement_rejects_a_duplicate_active_hold():
    existing = FakeHold('H1', 1, 'dee', '123', date(2026, 11, 1))

    result = application([existing], {'123': 'ana'}).place('dee', '123')

    assert result == HoldError(409, 'already on hold')


def test_fourth_active_hold_is_allowed_but_fifth_is_refused():
    holds = [FakeHold(f'H{i}', i, 'dee', str(i), date(2026, 11, 1)) for i in range(1, 4)]
    app = application(holds, {str(i): 'ana' for i in range(1, 6)})

    fourth = app.place('dee', '4')
    fifth = app.place('dee', '5')

    assert fourth.id == 'H4'
    assert fourth.placed_on == date(2026, 11, 23)
    assert app.list_active_text() == (
        'H1;dee;1;2026-11-01;2026-12-01\n'
        'H2;dee;2;2026-11-01;2026-12-01\n'
        'H3;dee;3;2026-11-01;2026-12-01\n'
        'H4;dee;4;2026-11-23;2026-12-23\n'
    )
    assert fifth == HoldError(409, 'hold limit reached')


def test_active_holds_are_ordered_filtered_and_include_the_expiry_date():
    app = application(
        [
            FakeHold('H2', 2, 'dee', '123', date(2026, 10, 24)),
            FakeHold('H1', 1, 'eli', '456', date(2026, 11, 1)),
            FakeHold('H3', 3, 'ana', '123', date(2026, 10, 23)),
            FakeHold('H4', 4, 'dee', '123', date(2026, 11, 1), date(2026, 11, 2)),
        ]
    )

    assert app.list_active_text() == (
        'H1;eli;456;2026-11-01;2026-12-01\nH2;dee;123;2026-10-24;2026-11-23\n'
    )
    assert app.list_active_text('missing') == '\n'


def test_cancellation_allows_expired_holds_and_rejects_repeat_cancellation():
    expired = FakeHold('H1', 1, 'dee', '123', date(2026, 1, 5))
    active = FakeHold('H2', 2, 'eli', '456', date(2026, 11, 1))
    app = application([expired, active])

    cancelled = app.cancel('H1')

    assert cancelled is expired
    assert cancelled.cancelled_on == date(2026, 11, 23)
    assert app.cancel('H1') == HoldError(409, 'hold already cancelled')
    assert app.list_active_text() == 'H2;eli;456;2026-11-01;2026-12-01\n'
    assert app.cancel('H2') is active
    assert app.list_active_text() == '\n'


def test_cancellation_of_unknown_hold_is_not_found():
    assert application().cancel('unknown') == HoldError(404, 'no such hold')
