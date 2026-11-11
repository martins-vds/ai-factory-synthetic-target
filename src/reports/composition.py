from src.fees.composition import fee_application

from .repository import DjangoMonthlyReportRepository
from .services import MonthlyReportApplication

monthly_report = MonthlyReportApplication(DjangoMonthlyReportRepository(), fee_application)
