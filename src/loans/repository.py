from django.db import transaction

from .models import Loan


class LoanRepository:
    def all(self):
        return Loan.objects.all()

    def find(self, loan_id):
        return Loan.objects.filter(pk=loan_id).first()

    @transaction.atomic
    def create(self, **fields):
        return Loan.objects.create(**fields)

    @transaction.atomic
    def mark_returned(self, loan_id, returned_on):
        loan = Loan.objects.select_for_update().filter(pk=loan_id).first()
        if loan is None or loan.returned_on is not None:
            return loan, False

        loan.returned_on = returned_on
        loan.save(update_fields=['returned_on'])
        return loan, True
