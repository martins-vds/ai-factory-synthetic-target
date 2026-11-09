import csv
from collections.abc import Iterable
from datetime import date
from io import StringIO
from typing import Protocol


class LoanRecord(Protocol):
    id: str
    member: str
    isbn: str
    lent_on: date
    due_on: date
    returned_on: date | None


class Clock(Protocol):
    def today(self) -> date: ...


class LoanRepository(Protocol):
    def all(self) -> Iterable[LoanRecord]: ...

    def find(self, loan_id: str) -> LoanRecord | None: ...

    def next_id(self) -> str: ...

    def create(self, *, id: str, member: str, isbn: str, lent_on: date) -> LoanRecord: ...

    def mark_returned(
        self, loan_id: str, returned_on: date
    ) -> tuple[LoanRecord | None, bool]: ...


class LoanApplication:
    def __init__(self, repository: LoanRepository, clock: Clock):
        self.repository = repository
        self.clock = clock

    def lend(self, member: str, isbn: str) -> LoanRecord:
        return self.repository.create(
            id=self.repository.next_id(),
            member=member,
            isbn=isbn,
            lent_on=self.clock.today(),
        )

    def return_loan(self, loan_id: str) -> tuple[LoanRecord | None, bool]:
        return self.repository.mark_returned(loan_id, self.clock.today())

    def list_loans_text(self) -> str:
        return ''.join(loan_line(loan) for loan in self.repository.all())

    def get_loan_text(self, loan_id: str) -> str | None:
        loan = self.repository.find(loan_id)
        return loan_line(loan) if loan else None


def loan_line(loan):
    output = StringIO(newline='')
    writer = csv.writer(output, delimiter=';', lineterminator='\n')
    writer.writerow(
        [
            loan.id,
            loan.member,
            loan.isbn,
            loan.lent_on.isoformat(),
            loan.due_on.isoformat(),
            loan.returned_on.isoformat() if loan.returned_on else '',
        ]
    )
    return output.getvalue()
