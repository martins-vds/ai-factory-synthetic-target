from collections.abc import Iterable
from contextlib import AbstractContextManager
from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import Protocol


class HoldRecord(Protocol):
    id: str
    sequence: int
    member: str
    isbn: str
    placed_on: date
    expires_on: date
    cancelled_on: date | None


class LoanState(Protocol):
    borrower: str


class LoanStateLookup(Protocol):
    def active_loan_for_isbn(self, isbn: str) -> LoanState | None: ...


class Clock(Protocol):
    def today(self) -> date: ...


@dataclass(frozen=True)
class HoldIdentity:
    id: str
    sequence: int


class HoldFailureCode(StrEnum):
    REQUIRED_FIELDS = 'required_fields'
    BOOK_AVAILABLE = 'book_available'
    BORROWER = 'borrower'
    DUPLICATE = 'duplicate'
    HOLD_LIMIT = 'hold_limit'
    NOT_FOUND = 'not_found'
    ALREADY_CANCELLED = 'already_cancelled'


@dataclass(frozen=True)
class HoldFailure:
    code: HoldFailureCode


class HoldRepository(Protocol):
    def placement(self) -> AbstractContextManager[None]: ...

    def active(self, isbn: str | None, today: date) -> Iterable[HoldRecord]: ...

    def active_count_for_member(self, member: str, today: date) -> int: ...

    def has_active_for_member_and_isbn(self, member: str, isbn: str, today: date) -> bool: ...

    def next_identity(self) -> HoldIdentity: ...

    def create(
        self, *, identity: HoldIdentity, member: str, isbn: str, placed_on: date
    ) -> HoldRecord: ...

    def find(self, hold_id: str) -> HoldRecord | None: ...

    def cancel(self, hold_id: str, cancelled_on: date) -> HoldRecord: ...


class HoldApplication:
    def __init__(
        self,
        repository: HoldRepository,
        clock: Clock,
        loan_state_lookup: LoanStateLookup,
    ):
        self.repository = repository
        self.clock = clock
        self.loan_state_lookup = loan_state_lookup

    def place(self, member: str, isbn: str) -> HoldRecord | HoldFailure:
        error = self._required_fields_error(member, isbn)
        if error is not None:
            return error

        with self.repository.placement():
            for check in (
                lambda: self._loan_error(member, isbn),
                lambda: self._duplicate_error(member, isbn),
                lambda: self._limit_error(member),
            ):
                error = check()
                if error is not None:
                    return error

            return self.repository.create(
                identity=self.repository.next_identity(),
                member=member,
                isbn=isbn,
                placed_on=self.clock.today(),
            )

    def _required_fields_error(self, member: str, isbn: str) -> HoldFailure | None:
        if not member or not member.strip() or not isbn or not isbn.strip():
            return HoldFailure(HoldFailureCode.REQUIRED_FIELDS)
        return None

    def _loan_error(self, member: str, isbn: str) -> HoldFailure | None:
        loan = self.loan_state_lookup.active_loan_for_isbn(isbn)
        if loan is None:
            return HoldFailure(HoldFailureCode.BOOK_AVAILABLE)
        if loan.borrower == member:
            return HoldFailure(HoldFailureCode.BORROWER)
        return None

    def _duplicate_error(self, member: str, isbn: str) -> HoldFailure | None:
        if self.repository.has_active_for_member_and_isbn(member, isbn, self.clock.today()):
            return HoldFailure(HoldFailureCode.DUPLICATE)
        return None

    def _limit_error(self, member: str) -> HoldFailure | None:
        if self.repository.active_count_for_member(member, self.clock.today()) > 3:
            return HoldFailure(HoldFailureCode.HOLD_LIMIT)
        return None

    def list_active(self, isbn: str | None = None) -> Iterable[HoldRecord]:
        return self.repository.active(isbn, self.clock.today())

    def list_active_text(self, isbn: str | None = None) -> str:
        return ''.join(hold_line(hold) for hold in self.list_active(isbn)) or '\n'

    def cancel(self, hold_id: str) -> HoldRecord | HoldFailure:
        hold = self.repository.find(hold_id)
        if hold is None:
            return HoldFailure(HoldFailureCode.NOT_FOUND)
        if hold.cancelled_on is not None:
            return HoldFailure(HoldFailureCode.ALREADY_CANCELLED)
        return self.repository.cancel(hold_id, self.clock.today())


def hold_line(hold: HoldRecord) -> str:
    return (
        f'{hold.id};{hold.member};{hold.isbn};{hold.placed_on.isoformat()};'
        f'{hold.expires_on.isoformat()}\n'
    )
