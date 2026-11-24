import csv
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from io import StringIO
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
    member: str


class LoanStateLookup(Protocol):
    def active_loan_for_isbn(self, isbn: str) -> LoanState | None: ...


class Clock(Protocol):
    def today(self) -> date: ...


@dataclass(frozen=True)
class HoldIdentity:
    id: str
    sequence: int


@dataclass(frozen=True)
class HoldError:
    status: int
    message: str


class HoldRepository(Protocol):
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

    def place(self, member: str, isbn: str) -> HoldRecord | HoldError:
        for check in (
            lambda: self._required_fields_error(member, isbn),
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

    def _required_fields_error(self, member: str, isbn: str) -> HoldError | None:
        if not member or not member.strip() or not isbn or not isbn.strip():
            return HoldError(400, 'member and isbn are required')
        return None

    def _loan_error(self, member: str, isbn: str) -> HoldError | None:
        loan = self.loan_state_lookup.active_loan_for_isbn(isbn)
        if loan is None:
            return HoldError(409, 'book is available')
        if loan.member == member:
            return HoldError(409, 'member has this book')
        return None

    def _duplicate_error(self, member: str, isbn: str) -> HoldError | None:
        if self.repository.has_active_for_member_and_isbn(member, isbn, self.clock.today()):
            return HoldError(409, 'already on hold')
        return None

    def _limit_error(self, member: str) -> HoldError | None:
        if self.repository.active_count_for_member(member, self.clock.today()) > 3:
            return HoldError(409, 'hold limit reached')
        return None

    def list_active(self, isbn: str | None = None) -> Iterable[HoldRecord]:
        return self.repository.active(isbn, self.clock.today())

    def list_active_text(self, isbn: str | None = None) -> str:
        return ''.join(hold_line(hold) for hold in self.list_active(isbn)) or '\n'

    def cancel(self, hold_id: str) -> HoldRecord | HoldError:
        hold = self.repository.find(hold_id)
        if hold is None:
            return HoldError(404, 'no such hold')
        if hold.cancelled_on is not None:
            return HoldError(409, 'hold already cancelled')
        return self.repository.cancel(hold_id, self.clock.today())


def hold_line(hold: HoldRecord) -> str:
    output = StringIO(newline='')
    writer = csv.writer(output, delimiter=';', lineterminator='\n')
    writer.writerow(
        [
            hold.id,
            hold.member,
            hold.isbn,
            hold.placed_on.isoformat(),
            hold.expires_on.isoformat(),
        ]
    )
    return output.getvalue()
