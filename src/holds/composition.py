from src.loans.composition import loan_application

from .clock import SystemClock
from .repository import DjangoHoldRepository
from .services import HoldApplication

hold_application = HoldApplication(
    DjangoHoldRepository(),
    SystemClock(),
    loan_application,
)
