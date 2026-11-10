from datetime import date

from django.utils import timezone


class SystemClock:
    def today(self) -> date:
        return timezone.localdate()
