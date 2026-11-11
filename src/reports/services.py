from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Protocol


class LoanRecord(Protocol):
    id: str
    member: str
    due_on: date
    returned_on: date | None


class FeeResult(Protocol):
    amount_cents: int


class FeeCalculator(Protocol):
    def fee_for(self, loan_id: str) -> FeeResult | None: ...


class MonthlyReportRepository(Protocol):
    def started_between(self, start: date, end: date) -> Iterable[LoanRecord]: ...


@dataclass(frozen=True)
class MemberMonthlyReport:
    member_id: str
    loans_started: int
    late_returns: int
    total_late_fees_cents: int


@dataclass
class _MemberTotals:
    loans_started: int = 0
    late_returns: int = 0
    total_late_fees_cents: int = 0


class MonthlyReportApplication:
    def __init__(self, loans: MonthlyReportRepository, fees: FeeCalculator):
        self.loans = loans
        self.fees = fees

    def for_previous_month(self, as_of: date) -> list[MemberMonthlyReport]:
        end = as_of.replace(day=1)
        start = (end - timedelta(days=1)).replace(day=1)
        totals: dict[str, _MemberTotals] = defaultdict(_MemberTotals)

        for loan in self.loans.started_between(start, end):
            member_totals = totals[loan.member]
            member_totals.loans_started += 1
            if loan.returned_on is not None and loan.returned_on > loan.due_on:
                member_totals.late_returns += 1

            fee = self.fees.fee_for(loan.id)
            if fee is not None:
                member_totals.total_late_fees_cents += fee.amount_cents

        return sorted(
            (
                MemberMonthlyReport(
                    member_id=member_id,
                    loans_started=member_totals.loans_started,
                    late_returns=member_totals.late_returns,
                    total_late_fees_cents=member_totals.total_late_fees_cents,
                )
                for member_id, member_totals in totals.items()
            ),
            key=lambda report: (-report.total_late_fees_cents, report.member_id),
        )
