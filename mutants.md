# Surviving mutants: HM-ACCEPT

Written by `afs-mutation` on its last run (base `all`): score 0.921, threshold 0.8, killed 406, survived 35. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

- `src/holds/services.py:31 Mutant #1`

  ```diff
  @@ -28,7 +28,7 @@
       def today(self) -> date: ...
  -@dataclass(frozen=True)
  +@dataclass(frozen=False)
   class HoldIdentity:
       id: str
       sequence: int
  ```

- `src/holds/services.py:38 Mutant #3`

  ```diff
  @@ -35,7 +35,7 @@
   class HoldFailureCode(StrEnum):
  -    REQUIRED_FIELDS = 'required_fields'
  +    REQUIRED_FIELDS = 'XXrequired_fieldsXX'
       BOOK_AVAILABLE = 'book_available'
       BORROWER = 'borrower'
       DUPLICATE = 'duplicate'
  ```

- `src/holds/services.py:39 Mutant #5`

  ```diff
  @@ -36,7 +36,7 @@
   class HoldFailureCode(StrEnum):
       REQUIRED_FIELDS = 'required_fields'
  -    BOOK_AVAILABLE = 'book_available'
  +    BOOK_AVAILABLE = 'XXbook_availableXX'
       BORROWER = 'borrower'
       DUPLICATE = 'duplicate'
       HOLD_LIMIT = 'hold_limit'
  ```

- `src/holds/services.py:40 Mutant #7`

  ```diff
  @@ -37,7 +37,7 @@
   class HoldFailureCode(StrEnum):
       REQUIRED_FIELDS = 'required_fields'
       BOOK_AVAILABLE = 'book_available'
  -    BORROWER = 'borrower'
  +    BORROWER = 'XXborrowerXX'
       DUPLICATE = 'duplicate'
       HOLD_LIMIT = 'hold_limit'
       NOT_FOUND = 'not_found'
  ```

- `src/holds/services.py:41 Mutant #9`

  ```diff
  @@ -38,7 +38,7 @@
       REQUIRED_FIELDS = 'required_fields'
       BOOK_AVAILABLE = 'book_available'
       BORROWER = 'borrower'
  -    DUPLICATE = 'duplicate'
  +    DUPLICATE = 'XXduplicateXX'
       HOLD_LIMIT = 'hold_limit'
       NOT_FOUND = 'not_found'
       ALREADY_CANCELLED = 'already_cancelled'
  ```

- `src/holds/services.py:42 Mutant #11`

  ```diff
  @@ -39,7 +39,7 @@
       BOOK_AVAILABLE = 'book_available'
       BORROWER = 'borrower'
       DUPLICATE = 'duplicate'
  -    HOLD_LIMIT = 'hold_limit'
  +    HOLD_LIMIT = 'XXhold_limitXX'
       NOT_FOUND = 'not_found'
       ALREADY_CANCELLED = 'already_cancelled'
  ```

- `src/holds/services.py:43 Mutant #13`

  ```diff
  @@ -40,7 +40,7 @@
       BORROWER = 'borrower'
       DUPLICATE = 'duplicate'
       HOLD_LIMIT = 'hold_limit'
  -    NOT_FOUND = 'not_found'
  +    NOT_FOUND = 'XXnot_foundXX'
       ALREADY_CANCELLED = 'already_cancelled'
  ```

- `src/holds/services.py:44 Mutant #15`

  ```diff
  @@ -41,7 +41,7 @@
       DUPLICATE = 'duplicate'
       HOLD_LIMIT = 'hold_limit'
       NOT_FOUND = 'not_found'
  -    ALREADY_CANCELLED = 'already_cancelled'
  +    ALREADY_CANCELLED = 'XXalready_cancelledXX'
   @dataclass(frozen=True)
  ```

- `src/holds/services.py:47 Mutant #17`

  ```diff
  @@ -44,7 +44,7 @@
       ALREADY_CANCELLED = 'already_cancelled'
  -@dataclass(frozen=True)
  +@dataclass(frozen=False)
   class HoldFailure:
       code: HoldFailureCode
  ```

- `src/loans/repository.py:23 Mutant #52`

  ```diff
  @@ -20,7 +20,6 @@
       def create(self, *, id, member, isbn, lent_on):
           return Loan.objects.create(id=id, member=member, isbn=isbn, lent_on=lent_on)
  -    @transaction.atomic
       def mark_returned(self, loan_id, returned_on):
           loan = Loan.objects.select_for_update().filter(pk=loan_id).first()
           if loan is None or loan.returned_on is not None:
  ```

- `src/loans/views.py:12 Mutant #1`

  ```diff
  @@ -9,7 +9,7 @@
   def loan_catalog(request):
  -    return render(request, 'loans/list.html', {'loans': Loan.objects.all()})
  +    return render(request, 'XXloans/list.htmlXX', {'loans': Loan.objects.all()})
   def loan_catalog_detail(request, loan_id):
  ```

- `src/loans/views.py:12 Mutant #2`

  ```diff
  @@ -9,7 +9,7 @@
   def loan_catalog(request):
  -    return render(request, 'loans/list.html', {'loans': Loan.objects.all()})
  +    return render(request, 'loans/list.html', {'XXloansXX': Loan.objects.all()})
   def loan_catalog_detail(request, loan_id):
  ```

- `src/holds/views.py:27 Mutant #107`

  ```diff
  @@ -24,7 +24,7 @@
   def hold_collection(request):
       if request.method == 'GET':
           return HttpResponse(
  -            hold_application.list_active_text(request.GET.get('isbn')),
  +            hold_application.list_active_text(request.GET.get('XXisbnXX')),
               content_type='text/plain',
           )
  ```

- `src/holds/views.py:28 Mutant #108`

  ```diff
  @@ -25,7 +25,7 @@
       if request.method == 'GET':
           return HttpResponse(
               hold_application.list_active_text(request.GET.get('isbn')),
  -            content_type='text/plain',
  +            content_type='XXtext/plainXX',
           )
       result = hold_application.place(
  ```

- `src/holds/views.py:32 Mutant #110`

  ```diff
  @@ -29,7 +29,7 @@
           )
       result = hold_application.place(
  -        request.POST.get('member', ''),
  +        request.POST.get('member', 'XXXX'),
           request.POST.get('isbn', ''),
       )
       if isinstance(result, HoldFailure):
  ```

- `src/holds/views.py:33 Mutant #112`

  ```diff
  @@ -30,7 +30,7 @@
       result = hold_application.place(
           request.POST.get('member', ''),
  -        request.POST.get('isbn', ''),
  +        request.POST.get('isbn', 'XXXX'),
       )
       if isinstance(result, HoldFailure):
           return _failure_response(result)
  ```

- `src/holds/views.py:45 Mutant #118`

  ```diff
  @@ -42,5 +42,5 @@
       result = hold_application.cancel(hold_id)
       if isinstance(result, HoldFailure):
           return _failure_response(result)
  -    return HttpResponse(hold_line(result), content_type='text/plain')
  +    return HttpResponse(hold_line(result), content_type='XXtext/plainXX')
  ```

- `src/reports/management/commands/monthly_report.py:11 Mutant #119`

  ```diff
  @@ -8,7 +8,7 @@
   class Command(BaseCommand):
  -    help = 'Produce the previous month lending report.'
  +    help = 'XXProduce the previous month lending report.XX'
       def handle(self, *args, **options):
           reports = monthly_report.for_previous_month(timezone.localdate())
  ```

- `src/reports/management/commands/monthly_report.py:11 Mutant #120`

  ```diff
  @@ -8,7 +8,7 @@
   class Command(BaseCommand):
  -    help = 'Produce the previous month lending report.'
  +    help = None
       def handle(self, *args, **options):
           reports = monthly_report.for_previous_month(timezone.localdate())
  ```

- `src/loans/services.py:36 Mutant #1`

  ```diff
  @@ -33,7 +33,7 @@
       def mark_returned(self, loan_id: str, returned_on: date) -> tuple[LoanRecord | None, bool]: ...
  -@dataclass(frozen=True)
  +@dataclass(frozen=False)
   class ActiveLoan:
       borrower: str
  ```

- `src/holds/repository.py:10 Mutant #15`

  ```diff
  @@ -7,7 +7,7 @@
   from .models import Hold
   from .services import HoldIdentity
  -_HOLD_PLACEMENT_LOCK = 0x484F4C44
  +_HOLD_PLACEMENT_LOCK = 1213156421
   class DjangoHoldRepository:
  ```

- `src/holds/repository.py:40 Mutant #34`

  ```diff
  @@ -37,7 +37,6 @@
           sequence = (Hold.objects.aggregate(maximum=Max('sequence'))['maximum'] or 0) + 1
           return HoldIdentity(f'H{sequence}', sequence)
  -    @transaction.atomic
       def create(self, *, identity, member, isbn, placed_on):
           return Hold.objects.create(
               id=identity.id,
  ```

- `src/fees/services.py:24 Mutant #39`

  ```diff
  @@ -21,7 +21,7 @@
       def charge(self, loan_id: str) -> 'GatewayResponse': ...
  -@dataclass(frozen=True)
  +@dataclass(frozen=False)
   class Fee:
       due_on: date
       days_late: int
  ```

- `src/fees/services.py:31 Mutant #41`

  ```diff
  @@ -28,7 +28,7 @@
       amount_cents: int
  -@dataclass(frozen=True)
  +@dataclass(frozen=False)
   class GatewayResponse:
       status: int
       body: str
  ```

- `src/holds/models.py:7 Mutant #62`

  ```diff
  @@ -4,7 +4,7 @@
   class Hold(models.Model):
  -    id = models.CharField(max_length=255, primary_key=True)
  +    id = models.CharField(max_length=256, primary_key=True)
       sequence = models.PositiveIntegerField(unique=True)
       member = models.CharField(max_length=255)
       isbn = models.CharField(max_length=255)
  ```

- `src/holds/models.py:8 Mutant #65`

  ```diff
  @@ -5,7 +5,7 @@
   class Hold(models.Model):
       id = models.CharField(max_length=255, primary_key=True)
  -    sequence = models.PositiveIntegerField(unique=True)
  +    sequence = models.PositiveIntegerField(unique=False)
       member = models.CharField(max_length=255)
       isbn = models.CharField(max_length=255)
       placed_on = models.DateField()
  ```

- `src/holds/models.py:9 Mutant #67`

  ```diff
  @@ -6,7 +6,7 @@
   class Hold(models.Model):
       id = models.CharField(max_length=255, primary_key=True)
       sequence = models.PositiveIntegerField(unique=True)
  -    member = models.CharField(max_length=255)
  +    member = models.CharField(max_length=256)
       isbn = models.CharField(max_length=255)
       placed_on = models.DateField()
       cancelled_on = models.DateField(null=True, blank=True)
  ```

- `src/holds/models.py:10 Mutant #69`

  ```diff
  @@ -7,7 +7,7 @@
       id = models.CharField(max_length=255, primary_key=True)
       sequence = models.PositiveIntegerField(unique=True)
       member = models.CharField(max_length=255)
  -    isbn = models.CharField(max_length=255)
  +    isbn = models.CharField(max_length=256)
       placed_on = models.DateField()
       cancelled_on = models.DateField(null=True, blank=True)
  ```

- `src/holds/models.py:12 Mutant #72`

  ```diff
  @@ -9,7 +9,7 @@
       member = models.CharField(max_length=255)
       isbn = models.CharField(max_length=255)
       placed_on = models.DateField()
  -    cancelled_on = models.DateField(null=True, blank=True)
  +    cancelled_on = models.DateField(null=False, blank=True)
       class Meta:
           ordering = ('sequence',)
  ```

- `src/holds/models.py:12 Mutant #73`

  ```diff
  @@ -9,7 +9,7 @@
       member = models.CharField(max_length=255)
       isbn = models.CharField(max_length=255)
       placed_on = models.DateField()
  -    cancelled_on = models.DateField(null=True, blank=True)
  +    cancelled_on = models.DateField(null=True, blank=False)
       class Meta:
           ordering = ('sequence',)
  ```

- `src/holds/models.py:15 Mutant #76`

  ```diff
  @@ -12,7 +12,7 @@
       cancelled_on = models.DateField(null=True, blank=True)
       class Meta:
  -        ordering = ('sequence',)
  +        ordering = None
       @property
       def expires_on(self):
  ```

- `src/loans/urls.py:9 Mutant #83`

  ```diff
  @@ -6,7 +6,7 @@
       path('loans', views.loan_collection),
       path('loans/<str:loan_id>/return', views.loan_return),
       path('loans/<str:loan_id>', views.loan_detail),
  -    path('ui/loans/', views.loan_catalog),
  +    path('XXui/loans/XX', views.loan_catalog),
       path('ui/loans/new/', views.loan_lend_page),
       path('ui/loans/<str:loan_id>/return/', views.loan_return_page),
       path('ui/loans/<str:loan_id>/', views.loan_catalog_detail),
  ```

- `src/reports/services.py:27 Mutant #1`

  ```diff
  @@ -24,7 +24,7 @@
       def started_between(self, start: date, end: date) -> Iterable[LoanRecord]: ...
  -@dataclass(frozen=True)
  +@dataclass(frozen=False)
   class MemberMonthlyReport:
       member_id: str
       loans_started: int
  ```

- `src/reports/services.py:35 Mutant #3`

  ```diff
  @@ -31,8 +31,6 @@
       late_returns: int
       total_late_fees_cents: int
  -
  -@dataclass
   class _MemberTotals:
       loans_started: int = 0
       late_returns: int = 0
  ```

- `src/reports/services.py:49 Mutant #15`

  ```diff
  @@ -46,7 +46,7 @@
       def for_previous_month(self, as_of: date) -> list[MemberMonthlyReport]:
           end = as_of.replace(day=1)
  -        start = (end - timedelta(days=1)).replace(day=1)
  +        start = (end - timedelta(days=2)).replace(day=1)
           totals: dict[str, _MemberTotals] = defaultdict(_MemberTotals)
           for loan in self.loans.started_between(start, end):
  ```

