from .repository import DjangoMonthlyReportRepository
from .services import MonthlyReportApplication

monthly_report = MonthlyReportApplication(DjangoMonthlyReportRepository())
