from dataclasses import dataclass
from datetime import date
from typing import Protocol


class LoanRecord(Protocol):
    id: str
    due_on: date
    returned_on: date | None


class LoanRepository(Protocol):
    def find(self, loan_id: str) -> LoanRecord | None: ...


class Clock(Protocol):
    def today(self) -> date: ...


class PaymentGateway(Protocol):
    def charge(self, loan_id: str) -> 'GatewayResponse': ...


@dataclass(frozen=True)
class Fee:
    due_on: date
    days_late: int
    amount_cents: int


@dataclass(frozen=True)
class GatewayResponse:
    status: int
    body: str


class PaymentGatewayFailure(Exception):
    def __init__(self, body: str):
        super().__init__(body)
        self.body = body


class FeeApplication:
    def __init__(self, loans: LoanRepository, clock: Clock, gateway: PaymentGateway):
        self.loans = loans
        self.clock = clock
        self.gateway = gateway

    def fee_for(self, loan_id: str) -> Fee | None:
        loan = self.loans.find(loan_id)
        if loan is None:
            return None

        end = loan.returned_on if loan.returned_on is not None else self.clock.today()
        days_late = max(0, (end - loan.due_on).days)
        amount_cents = 0 if days_late <= 2 else min(1000, days_late * 25)
        return Fee(loan.due_on, days_late, amount_cents)

    def pay(self, loan_id: str) -> GatewayResponse | None:
        if self.loans.find(loan_id) is None:
            return None
        return self.gateway.charge(loan_id)
