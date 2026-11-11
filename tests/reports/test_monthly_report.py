import csv
from datetime import date
from io import StringIO

import pytest
from django.core.management import call_command

from src.loans.models import Loan


@pytest.mark.django_db
def test_monthly_report_summarizes_previous_month_loans_in_specified_order(monkeypatch):
    Loan.objects.all().delete()
    Loan.objects.bulk_create(
        [
            Loan(
                id='L-alpha',
                member='alpha',
                isbn='1',
                lent_on=date(2026, 2, 1),
                returned_on=date(2026, 2, 25),
            ),
            Loan(
                id='L-beta',
                member='beta',
                isbn='2',
                lent_on=date(2026, 2, 2),
                returned_on=date(2026, 2, 26),
            ),
            Loan(
                id='L-zeta-1',
                member='zeta',
                isbn='3',
                lent_on=date(2026, 2, 3),
                returned_on=date(2026, 2, 20),
            ),
            Loan(
                id='L-zeta-2',
                member='zeta',
                isbn='4',
                lent_on=date(2026, 2, 4),
                returned_on=date(2026, 2, 18),
            ),
            Loan(
                id='L-zeta-3',
                member='zeta',
                isbn='7',
                lent_on=date(2026, 2, 5),
                returned_on=date(2026, 2, 20),
            ),
            Loan(
                id='L-before',
                member='before',
                isbn='5',
                lent_on=date(2026, 1, 31),
            ),
            Loan(
                id='L-after',
                member='after',
                isbn='6',
                lent_on=date(2026, 3, 1),
            ),
        ]
    )
    monkeypatch.setattr(
        'src.reports.management.commands.monthly_report.timezone.localdate',
        lambda: date(2026, 3, 1),
    )
    output = StringIO()

    call_command('monthly_report', stdout=output)

    assert list(csv.reader(StringIO(output.getvalue()))) == [
        ['member_id', 'loans_started', 'late_returns', 'total_late_fees_cents'],
        ['alpha', '1', '1', '250'],
        ['beta', '1', '1', '250'],
        ['zeta', '3', '2', '75'],
    ]


@pytest.mark.django_db
def test_monthly_report_uses_previous_calendar_year_for_january_run(monkeypatch):
    Loan.objects.all().delete()
    Loan.objects.create(
        id='L-december',
        member='dee',
        isbn='1',
        lent_on=date(2025, 12, 1),
    )
    monkeypatch.setattr(
        'src.reports.management.commands.monthly_report.timezone.localdate',
        lambda: date(2026, 1, 1),
    )
    output = StringIO()

    call_command('monthly_report', stdout=output)

    assert list(csv.reader(StringIO(output.getvalue()))) == [
        ['member_id', 'loans_started', 'late_returns', 'total_late_fees_cents'],
        ['dee', '1', '0', '425'],
    ]
