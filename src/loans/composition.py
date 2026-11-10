from .clock import SystemClock
from .repository import DjangoLoanRepository
from .services import LoanApplication

loan_application = LoanApplication(DjangoLoanRepository(), SystemClock())
