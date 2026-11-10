from django.db import transaction

from .models import Loan


class DjangoLoanRepository:
    def all(self):
        return Loan.objects.all()

    def find(self, loan_id):
        return Loan.objects.filter(pk=loan_id).first()

    def next_id(self):
        return f'L{Loan.objects.count() + 1}'

    @transaction.atomic
    def create(self, *, id, member, isbn, lent_on):
        return Loan.objects.create(id=id, member=member, isbn=isbn, lent_on=lent_on)

    @transaction.atomic
    def mark_returned(self, loan_id, returned_on):
        loan = Loan.objects.select_for_update().filter(pk=loan_id).first()
        if loan is None or loan.returned_on is not None:
            return loan, False

        loan.returned_on = returned_on
        loan.save(update_fields=['returned_on'])
        return loan, True
