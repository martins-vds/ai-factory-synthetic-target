from datetime import timedelta

from django.db import transaction
from django.db.models import Max

from .models import Hold
from .services import HoldIdentity


class DjangoHoldRepository:
    def active(self, isbn, today):
        holds = Hold.objects.filter(
            cancelled_on__isnull=True,
            placed_on__gte=today - timedelta(days=30),
        )
        if isbn is not None:
            holds = holds.filter(isbn=isbn)
        return holds.order_by('sequence')

    def active_count_for_member(self, member, today):
        return self.active(None, today).filter(member=member).count()

    def has_active_for_member_and_isbn(self, member, isbn, today):
        return self.active(isbn, today).filter(member=member).exists()

    def next_identity(self):
        sequence = (Hold.objects.aggregate(maximum=Max('sequence'))['maximum'] or 0) + 1
        return HoldIdentity(f'H{sequence}', sequence)

    @transaction.atomic
    def create(self, *, identity, member, isbn, placed_on):
        return Hold.objects.create(
            id=identity.id,
            sequence=identity.sequence,
            member=member,
            isbn=isbn,
            placed_on=placed_on,
        )

    def find(self, hold_id):
        return Hold.objects.filter(pk=hold_id).first()

    @transaction.atomic
    def cancel(self, hold_id, cancelled_on):
        hold = Hold.objects.select_for_update().get(pk=hold_id)
        hold.cancelled_on = cancelled_on
        hold.save(update_fields=['cancelled_on'])
        return hold
