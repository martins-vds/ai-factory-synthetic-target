from django.db import transaction

from .models import Loan


class LoanRepository:
    @staticmethod
    def all():
        return Loan.objects.all()

    @staticmethod
    def find(loan_id):
        return Loan.objects.filter(pk=loan_id).first()

    @staticmethod
    @transaction.atomic
    def create(**fields):
        return Loan.objects.create(**fields)
