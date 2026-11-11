from src.loans.models import Loan


class DjangoFeeLoanRepository:
    def find(self, loan_id):
        return Loan.objects.filter(pk=loan_id).first()
