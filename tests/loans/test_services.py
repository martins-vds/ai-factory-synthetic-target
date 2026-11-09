from dataclasses import dataclass
from datetime import date, timedelta

from src.loans.services import LoanApplication


@dataclass
class InMemoryLoan:
    id: str
    member: str
    isbn: str
    lent_on: date
    returned_on: date | None = None

    @property
    def due_on(self):
        return self.lent_on + timedelta(days=14)


class InMemoryLoanRepository:
    def __init__(self):
        self.loans = {}

    def next_id(self):
        return f'L{len(self.loans) + 1}'

    def create(self, **fields):
        loan = InMemoryLoan(**fields)
        self.loans[loan.id] = loan
        return loan

    def mark_returned(self, loan_id, returned_on):
        loan = self.loans.get(loan_id)
        if loan is None or loan.returned_on is not None:
            return loan, False
        loan.returned_on = returned_on
        return loan, True


class FixedClock:
    def today(self):
        return date(2026, 11, 9)


def test_lending_use_case_uses_injected_repository_and_clock():
    repository = InMemoryLoanRepository()
    application = LoanApplication(repository, FixedClock())

    loan = application.lend('dee', '123')

    assert (loan.id, loan.member, loan.isbn) == ('L1', 'dee', '123')
    assert loan.lent_on == date(2026, 11, 9)
    assert loan.due_on == date(2026, 11, 23)


def test_return_use_case_uses_injected_clock_and_preserves_repeat_date():
    repository = InMemoryLoanRepository()
    repository.create(
        id='L1',
        member='dee',
        isbn='123',
        lent_on=date(2026, 10, 1),
    )
    application = LoanApplication(repository, FixedClock())

    loan, updated = application.return_loan('L1')
    repeated_loan, repeated_update = application.return_loan('L1')

    assert updated is True
    assert loan.returned_on == date(2026, 11, 9)
    assert repeated_update is False
    assert repeated_loan.returned_on == date(2026, 11, 9)
