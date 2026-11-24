from datetime import timedelta

from django.db import models


class Hold(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    sequence = models.PositiveIntegerField(unique=True)
    member = models.CharField(max_length=255)
    isbn = models.CharField(max_length=255)
    placed_on = models.DateField()
    cancelled_on = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('sequence',)

    @property
    def expires_on(self):
        return self.placed_on + timedelta(days=30)
