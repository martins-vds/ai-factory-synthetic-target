from src.loans.clock import SystemClock

from .gateway import HttpPaymentGateway
from .repository import DjangoFeeLoanRepository
from .services import FeeApplication

fee_application = FeeApplication(
    DjangoFeeLoanRepository(),
    SystemClock(),
    HttpPaymentGateway(),
)
