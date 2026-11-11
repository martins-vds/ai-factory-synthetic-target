import csv
from io import StringIO

from django.core.management.base import BaseCommand
from django.utils import timezone

from src.reports.composition import monthly_report


class Command(BaseCommand):
    help = 'Produce the previous month lending report.'

    def handle(self, *args, **options):
        reports = monthly_report.for_previous_month(timezone.localdate())
        output = StringIO(newline='')
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(['member_id', 'loans_started', 'late_returns', 'total_late_fees_cents'])
        for report in reports:
            writer.writerow(
                [
                    report.member_id,
                    report.loans_started,
                    report.late_returns,
                    report.total_late_fees_cents,
                ]
            )
        self.stdout.write(output.getvalue(), ending='')
