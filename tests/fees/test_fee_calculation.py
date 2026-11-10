from dataclasses import dataclass
from datetime import date, timedelta

import pytest

from src.fees.services import FeeApplication, GatewayResponse


@dataclass
class Loan:
    id: str
    due_on: date
    returned_on: date | None = None


class LoanRepository:
    def __init__(self, loan):
        self.loan = loan

    def find(self, loan_id):
        return self.loan if self.loan and self.loan.id == loan_id else None


class Clock:
    def __init__(self, today):
        self.value = today

    def today(self):
        return self.value


class PaymentGateway:
    def charge(self, loan_id):
        raise AssertionError('fee calculation must not charge the gateway')


class RecordingPaymentGateway:
    def __init__(self):
        self.loan_ids = []

    def charge(self, loan_id):
        self.loan_ids.append(loan_id)
        return GatewayResponse(200, 'charged\n')


@pytest.mark.parametrize(
    ('days_late', 'expected_cents'),
    [(0, 0), (1, 0), (2, 0), (3, 75), (11, 275), (100, 1000)],
)
def test_fee_calculates_unreturned_loan_with_grace_period_and_cap(days_late, expected_cents):
    due_on = date(2026, 1, 10)
    application = FeeApplication(
        LoanRepository(Loan('L1', due_on)),
        Clock(date(2026, 1, 10) + timedelta(days=days_late)),
        PaymentGateway(),
    )

    fee = application.fee_for('L1')

    assert fee.due_on == due_on
    assert fee.days_late == days_late
    assert fee.amount_cents == expected_cents


def test_fee_for_returned_loan_uses_return_date_instead_of_today():
    application = FeeApplication(
        LoanRepository(Loan('L1', date(2026, 1, 10), date(2026, 1, 13))),
        Clock(date(2026, 4, 1)),
        PaymentGateway(),
    )

    fee = application.fee_for('L1')

    assert fee.days_late == 3
    assert fee.amount_cents == 75


def test_fee_for_unknown_loan_returns_none():
    application = FeeApplication(LoanRepository(None), Clock(date(2026, 1, 1)), PaymentGateway())

    assert application.fee_for('missing') is None


def test_pay_existing_loan_uses_gateway_port():
    gateway = RecordingPaymentGateway()
    application = FeeApplication(
        LoanRepository(Loan('L1', date(2026, 1, 10))),
        Clock(date(2026, 1, 10)),
        gateway,
    )

    response = application.pay('L1')

    assert response == GatewayResponse(200, 'charged\n')
    assert gateway.loan_ids == ['L1']


def test_pay_unknown_loan_does_not_use_gateway_port():
    gateway = RecordingPaymentGateway()
    application = FeeApplication(LoanRepository(None), Clock(date(2026, 1, 1)), gateway)

    assert application.pay('missing') is None
    assert gateway.loan_ids == []
