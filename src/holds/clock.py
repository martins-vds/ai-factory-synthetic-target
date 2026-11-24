from django.utils import timezone


class SystemClock:
    def today(self):
        return timezone.localdate()
