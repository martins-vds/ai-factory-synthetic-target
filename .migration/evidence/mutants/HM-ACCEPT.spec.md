# Surviving mutants (customer spec only): HM-ACCEPT

Written by `afs-mutation` on its last run (base `all`): score 0.510, threshold 0.8, killed 225, survived 216. Each line is a mutant no customer spec case killed: add a spec case (Characterizer) that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

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

- `src/holds/services.py:106 Mutant #33`

  ```diff
  @@ -103,7 +103,7 @@
               )
       def _required_fields_error(self, member: str, isbn: str) -> HoldFailure | None:
  -        if not member or not member.strip() or not isbn or not isbn.strip():
  +        if not member and not member.strip() or not isbn or not isbn.strip():
               return HoldFailure(HoldFailureCode.REQUIRED_FIELDS)
           return None
  ```

- `src/loans/repository.py:19 Mutant #51`

  ```diff
  @@ -16,7 +16,6 @@
       def next_id(self):
           return f'L{Loan.objects.count() + 1}'
  -    @transaction.atomic
       def create(self, *, id, member, isbn, lent_on):
           return Loan.objects.create(id=id, member=member, isbn=isbn, lent_on=lent_on)
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

- `src/loans/repository.py:26 Mutant #56`

  ```diff
  @@ -23,7 +23,7 @@
       @transaction.atomic
       def mark_returned(self, loan_id, returned_on):
           loan = Loan.objects.select_for_update().filter(pk=loan_id).first()
  -        if loan is None or loan.returned_on is not None:
  +        if loan is None and loan.returned_on is not None:
               return loan, False
           loan.returned_on = returned_on
  ```

- `src/loans/repository.py:27 Mutant #57`

  ```diff
  @@ -24,7 +24,7 @@
       def mark_returned(self, loan_id, returned_on):
           loan = Loan.objects.select_for_update().filter(pk=loan_id).first()
           if loan is None or loan.returned_on is not None:
  -            return loan, False
  +            return loan, True
           loan.returned_on = returned_on
           loan.save(update_fields=['returned_on'])
  ```

- `src/reports/composition.py:6 Mutant #80`

  ```diff
  @@ -3,5 +3,5 @@
   from .repository import DjangoMonthlyReportRepository
   from .services import MonthlyReportApplication
  -monthly_report = MonthlyReportApplication(DjangoMonthlyReportRepository(), fee_application)
  +monthly_report = None
  ```

- `src/core/database.py:6 Mutant #81`

  ```diff
  @@ -3,6 +3,6 @@
   def database_probe() -> int:
       with connection.cursor() as cursor:
  -        cursor.execute('SELECT 1')
  +        cursor.execute('XXSELECT 1XX')
           return cursor.fetchone()[0]
  ```

- `src/core/database.py:7 Mutant #82`

  ```diff
  @@ -4,5 +4,5 @@
   def database_probe() -> int:
       with connection.cursor() as cursor:
           cursor.execute('SELECT 1')
  -        return cursor.fetchone()[0]
  +        return cursor.fetchone()[1]
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

- `src/loans/views.py:16 Mutant #3`

  ```diff
  @@ -13,7 +13,7 @@
   def loan_catalog_detail(request, loan_id):
  -    loan = get_object_or_404(Loan, pk=loan_id)
  +    loan = None
       return render(request, 'loans/detail.html', {'loan': loan})
  ```

- `src/loans/views.py:17 Mutant #4`

  ```diff
  @@ -14,7 +14,7 @@
   def loan_catalog_detail(request, loan_id):
       loan = get_object_or_404(Loan, pk=loan_id)
  -    return render(request, 'loans/detail.html', {'loan': loan})
  +    return render(request, 'XXloans/detail.htmlXX', {'loan': loan})
   @require_http_methods(['GET', 'POST'])
  ```

- `src/loans/views.py:17 Mutant #5`

  ```diff
  @@ -14,7 +14,7 @@
   def loan_catalog_detail(request, loan_id):
       loan = get_object_or_404(Loan, pk=loan_id)
  -    return render(request, 'loans/detail.html', {'loan': loan})
  +    return render(request, 'loans/detail.html', {'XXloanXX': loan})
   @require_http_methods(['GET', 'POST'])
  ```

- `src/loans/views.py:20 Mutant #6`

  ```diff
  @@ -17,7 +17,7 @@
       return render(request, 'loans/detail.html', {'loan': loan})
  -@require_http_methods(['GET', 'POST'])
  +@require_http_methods(['XXGETXX', 'POST'])
   def loan_collection(request):
       if request.method == 'POST':
           return loan_lend(request)
  ```

- `src/loans/views.py:20 Mutant #8`

  ```diff
  @@ -16,8 +16,6 @@
       loan = get_object_or_404(Loan, pk=loan_id)
       return render(request, 'loans/detail.html', {'loan': loan})
  -
  -@require_http_methods(['GET', 'POST'])
   def loan_collection(request):
       if request.method == 'POST':
           return loan_lend(request)
  ```

- `src/loans/views.py:24 Mutant #11`

  ```diff
  @@ -21,7 +21,7 @@
   def loan_collection(request):
       if request.method == 'POST':
           return loan_lend(request)
  -    return HttpResponse(loan_application.list_loans_text(), content_type='text/plain')
  +    return HttpResponse(loan_application.list_loans_text(), content_type='XXtext/plainXX')
   def loan_lend(request):
  ```

- `src/loans/views.py:30 Mutant #14`

  ```diff
  @@ -27,7 +27,7 @@
   def loan_lend(request):
       form = LoanForm(request.POST)
       if not form.is_valid():
  -        errors = '\n'.join(
  +        errors = 'XX\nXX'.join(
               f'{field}: {message}' for field, messages in form.errors.items() for message in messages
           )
           return HttpResponse(errors, status=400, content_type='text/plain')
  ```

- `src/loans/views.py:31 Mutant #15`

  ```diff
  @@ -28,7 +28,7 @@
       form = LoanForm(request.POST)
       if not form.is_valid():
           errors = '\n'.join(
  -            f'{field}: {message}' for field, messages in form.errors.items() for message in messages
  +            f'XX{field}: {message}XX' for field, messages in form.errors.items() for message in messages
           )
           return HttpResponse(errors, status=400, content_type='text/plain')
  ```

- `src/loans/views.py:32 Mutant #16`

  ```diff
  @@ -27,9 +27,7 @@
   def loan_lend(request):
       form = LoanForm(request.POST)
       if not form.is_valid():
  -        errors = '\n'.join(
  -            f'{field}: {message}' for field, messages in form.errors.items() for message in messages
  -        )
  +        errors = None
           return HttpResponse(errors, status=400, content_type='text/plain')
       loan = loan_application.lend(**form.cleaned_data)
  ```

- `src/loans/views.py:33 Mutant #17`

  ```diff
  @@ -30,7 +30,7 @@
           errors = '\n'.join(
               f'{field}: {message}' for field, messages in form.errors.items() for message in messages
           )
  -        return HttpResponse(errors, status=400, content_type='text/plain')
  +        return HttpResponse(errors, status=401, content_type='text/plain')
       loan = loan_application.lend(**form.cleaned_data)
       return HttpResponse(loan_line(loan), status=201, content_type='text/plain')
  ```

- `src/loans/views.py:33 Mutant #18`

  ```diff
  @@ -30,7 +30,7 @@
           errors = '\n'.join(
               f'{field}: {message}' for field, messages in form.errors.items() for message in messages
           )
  -        return HttpResponse(errors, status=400, content_type='text/plain')
  +        return HttpResponse(errors, status=400, content_type='XXtext/plainXX')
       loan = loan_application.lend(**form.cleaned_data)
       return HttpResponse(loan_line(loan), status=201, content_type='text/plain')
  ```

- `src/loans/views.py:36 Mutant #20`

  ```diff
  @@ -33,7 +33,7 @@
           return HttpResponse(errors, status=400, content_type='text/plain')
       loan = loan_application.lend(**form.cleaned_data)
  -    return HttpResponse(loan_line(loan), status=201, content_type='text/plain')
  +    return HttpResponse(loan_line(loan), status=202, content_type='text/plain')
   @require_http_methods(['GET', 'POST'])
  ```

- `src/loans/views.py:36 Mutant #21`

  ```diff
  @@ -33,7 +33,7 @@
           return HttpResponse(errors, status=400, content_type='text/plain')
       loan = loan_application.lend(**form.cleaned_data)
  -    return HttpResponse(loan_line(loan), status=201, content_type='text/plain')
  +    return HttpResponse(loan_line(loan), status=201, content_type='XXtext/plainXX')
   @require_http_methods(['GET', 'POST'])
  ```

- `src/loans/views.py:39 Mutant #22`

  ```diff
  @@ -36,7 +36,7 @@
       return HttpResponse(loan_line(loan), status=201, content_type='text/plain')
  -@require_http_methods(['GET', 'POST'])
  +@require_http_methods(['XXGETXX', 'POST'])
   def loan_lend_page(request):
       form = LoanForm(request.POST if request.method == 'POST' else None)
       if request.method == 'POST' and form.is_valid():
  ```

- `src/loans/views.py:39 Mutant #23`

  ```diff
  @@ -36,7 +36,7 @@
       return HttpResponse(loan_line(loan), status=201, content_type='text/plain')
  -@require_http_methods(['GET', 'POST'])
  +@require_http_methods(['GET', 'XXPOSTXX'])
   def loan_lend_page(request):
       form = LoanForm(request.POST if request.method == 'POST' else None)
       if request.method == 'POST' and form.is_valid():
  ```

- `src/loans/views.py:39 Mutant #24`

  ```diff
  @@ -35,8 +35,6 @@
       loan = loan_application.lend(**form.cleaned_data)
       return HttpResponse(loan_line(loan), status=201, content_type='text/plain')
  -
  -@require_http_methods(['GET', 'POST'])
   def loan_lend_page(request):
       form = LoanForm(request.POST if request.method == 'POST' else None)
       if request.method == 'POST' and form.is_valid():
  ```

- `src/loans/views.py:41 Mutant #25`

  ```diff
  @@ -38,7 +38,7 @@
   @require_http_methods(['GET', 'POST'])
   def loan_lend_page(request):
  -    form = LoanForm(request.POST if request.method == 'POST' else None)
  +    form = LoanForm(request.POST if request.method != 'POST' else None)
       if request.method == 'POST' and form.is_valid():
           loan = loan_application.lend(**form.cleaned_data)
           if request.headers.get('HX-Request') == 'true':
  ```

- `src/loans/views.py:41 Mutant #26`

  ```diff
  @@ -38,7 +38,7 @@
   @require_http_methods(['GET', 'POST'])
   def loan_lend_page(request):
  -    form = LoanForm(request.POST if request.method == 'POST' else None)
  +    form = LoanForm(request.POST if request.method == 'XXPOSTXX' else None)
       if request.method == 'POST' and form.is_valid():
           loan = loan_application.lend(**form.cleaned_data)
           if request.headers.get('HX-Request') == 'true':
  ```

- `src/loans/views.py:41 Mutant #27`

  ```diff
  @@ -38,7 +38,7 @@
   @require_http_methods(['GET', 'POST'])
   def loan_lend_page(request):
  -    form = LoanForm(request.POST if request.method == 'POST' else None)
  +    form = None
       if request.method == 'POST' and form.is_valid():
           loan = loan_application.lend(**form.cleaned_data)
           if request.headers.get('HX-Request') == 'true':
  ```

- `src/loans/views.py:42 Mutant #28`

  ```diff
  @@ -39,7 +39,7 @@
   @require_http_methods(['GET', 'POST'])
   def loan_lend_page(request):
       form = LoanForm(request.POST if request.method == 'POST' else None)
  -    if request.method == 'POST' and form.is_valid():
  +    if request.method != 'POST' and form.is_valid():
           loan = loan_application.lend(**form.cleaned_data)
           if request.headers.get('HX-Request') == 'true':
               return render(request, 'loans/loan-created.html', {'loan': loan})
  ```

- `src/loans/views.py:42 Mutant #29`

  ```diff
  @@ -39,7 +39,7 @@
   @require_http_methods(['GET', 'POST'])
   def loan_lend_page(request):
       form = LoanForm(request.POST if request.method == 'POST' else None)
  -    if request.method == 'POST' and form.is_valid():
  +    if request.method == 'XXPOSTXX' and form.is_valid():
           loan = loan_application.lend(**form.cleaned_data)
           if request.headers.get('HX-Request') == 'true':
               return render(request, 'loans/loan-created.html', {'loan': loan})
  ```

- `src/loans/views.py:42 Mutant #30`

  ```diff
  @@ -39,7 +39,7 @@
   @require_http_methods(['GET', 'POST'])
   def loan_lend_page(request):
       form = LoanForm(request.POST if request.method == 'POST' else None)
  -    if request.method == 'POST' and form.is_valid():
  +    if request.method == 'POST' or form.is_valid():
           loan = loan_application.lend(**form.cleaned_data)
           if request.headers.get('HX-Request') == 'true':
               return render(request, 'loans/loan-created.html', {'loan': loan})
  ```

- `src/loans/views.py:43 Mutant #31`

  ```diff
  @@ -40,7 +40,7 @@
   def loan_lend_page(request):
       form = LoanForm(request.POST if request.method == 'POST' else None)
       if request.method == 'POST' and form.is_valid():
  -        loan = loan_application.lend(**form.cleaned_data)
  +        loan = None
           if request.headers.get('HX-Request') == 'true':
               return render(request, 'loans/loan-created.html', {'loan': loan})
           return redirect(f'/ui/loans/{loan.id}/')
  ```

- `src/loans/views.py:44 Mutant #32`

  ```diff
  @@ -41,7 +41,7 @@
       form = LoanForm(request.POST if request.method == 'POST' else None)
       if request.method == 'POST' and form.is_valid():
           loan = loan_application.lend(**form.cleaned_data)
  -        if request.headers.get('HX-Request') == 'true':
  +        if request.headers.get('XXHX-RequestXX') == 'true':
               return render(request, 'loans/loan-created.html', {'loan': loan})
           return redirect(f'/ui/loans/{loan.id}/')
       template = (
  ```

- `src/loans/views.py:44 Mutant #33`

  ```diff
  @@ -41,7 +41,7 @@
       form = LoanForm(request.POST if request.method == 'POST' else None)
       if request.method == 'POST' and form.is_valid():
           loan = loan_application.lend(**form.cleaned_data)
  -        if request.headers.get('HX-Request') == 'true':
  +        if request.headers.get('HX-Request') != 'true':
               return render(request, 'loans/loan-created.html', {'loan': loan})
           return redirect(f'/ui/loans/{loan.id}/')
       template = (
  ```

- `src/loans/views.py:44 Mutant #34`

  ```diff
  @@ -41,7 +41,7 @@
       form = LoanForm(request.POST if request.method == 'POST' else None)
       if request.method == 'POST' and form.is_valid():
           loan = loan_application.lend(**form.cleaned_data)
  -        if request.headers.get('HX-Request') == 'true':
  +        if request.headers.get('HX-Request') == 'XXtrueXX':
               return render(request, 'loans/loan-created.html', {'loan': loan})
           return redirect(f'/ui/loans/{loan.id}/')
       template = (
  ```

- `src/loans/views.py:45 Mutant #35`

  ```diff
  @@ -42,7 +42,7 @@
       if request.method == 'POST' and form.is_valid():
           loan = loan_application.lend(**form.cleaned_data)
           if request.headers.get('HX-Request') == 'true':
  -            return render(request, 'loans/loan-created.html', {'loan': loan})
  +            return render(request, 'XXloans/loan-created.htmlXX', {'loan': loan})
           return redirect(f'/ui/loans/{loan.id}/')
       template = (
           'loans/loan-form.html'
  ```

- `src/loans/views.py:45 Mutant #36`

  ```diff
  @@ -42,7 +42,7 @@
       if request.method == 'POST' and form.is_valid():
           loan = loan_application.lend(**form.cleaned_data)
           if request.headers.get('HX-Request') == 'true':
  -            return render(request, 'loans/loan-created.html', {'loan': loan})
  +            return render(request, 'loans/loan-created.html', {'XXloanXX': loan})
           return redirect(f'/ui/loans/{loan.id}/')
       template = (
           'loans/loan-form.html'
  ```

- `src/loans/views.py:46 Mutant #37`

  ```diff
  @@ -43,7 +43,7 @@
           loan = loan_application.lend(**form.cleaned_data)
           if request.headers.get('HX-Request') == 'true':
               return render(request, 'loans/loan-created.html', {'loan': loan})
  -        return redirect(f'/ui/loans/{loan.id}/')
  +        return redirect(f'XX/ui/loans/{loan.id}/XX')
       template = (
           'loans/loan-form.html'
           if request.method == 'POST' and request.headers.get('HX-Request') == 'true'
  ```

- `src/loans/views.py:48 Mutant #38`

  ```diff
  @@ -45,7 +45,7 @@
               return render(request, 'loans/loan-created.html', {'loan': loan})
           return redirect(f'/ui/loans/{loan.id}/')
       template = (
  -        'loans/loan-form.html'
  +        'XXloans/loan-form.htmlXX'
           if request.method == 'POST' and request.headers.get('HX-Request') == 'true'
           else 'loans/new.html'
       )
  ```

- `src/loans/views.py:49 Mutant #39`

  ```diff
  @@ -46,7 +46,7 @@
           return redirect(f'/ui/loans/{loan.id}/')
       template = (
           'loans/loan-form.html'
  -        if request.method == 'POST' and request.headers.get('HX-Request') == 'true'
  +        if request.method != 'POST' and request.headers.get('HX-Request') == 'true'
           else 'loans/new.html'
       )
       return render(request, template, {'form': form})
  ```

- `src/loans/views.py:49 Mutant #40`

  ```diff
  @@ -46,7 +46,7 @@
           return redirect(f'/ui/loans/{loan.id}/')
       template = (
           'loans/loan-form.html'
  -        if request.method == 'POST' and request.headers.get('HX-Request') == 'true'
  +        if request.method == 'XXPOSTXX' and request.headers.get('HX-Request') == 'true'
           else 'loans/new.html'
       )
       return render(request, template, {'form': form})
  ```

- `src/loans/views.py:49 Mutant #41`

  ```diff
  @@ -46,7 +46,7 @@
           return redirect(f'/ui/loans/{loan.id}/')
       template = (
           'loans/loan-form.html'
  -        if request.method == 'POST' and request.headers.get('HX-Request') == 'true'
  +        if request.method == 'POST' and request.headers.get('XXHX-RequestXX') == 'true'
           else 'loans/new.html'
       )
       return render(request, template, {'form': form})
  ```

- `src/loans/views.py:49 Mutant #42`

  ```diff
  @@ -46,7 +46,7 @@
           return redirect(f'/ui/loans/{loan.id}/')
       template = (
           'loans/loan-form.html'
  -        if request.method == 'POST' and request.headers.get('HX-Request') == 'true'
  +        if request.method == 'POST' and request.headers.get('HX-Request') != 'true'
           else 'loans/new.html'
       )
       return render(request, template, {'form': form})
  ```

- `src/loans/views.py:49 Mutant #43`

  ```diff
  @@ -46,7 +46,7 @@
           return redirect(f'/ui/loans/{loan.id}/')
       template = (
           'loans/loan-form.html'
  -        if request.method == 'POST' and request.headers.get('HX-Request') == 'true'
  +        if request.method == 'POST' and request.headers.get('HX-Request') == 'XXtrueXX'
           else 'loans/new.html'
       )
       return render(request, template, {'form': form})
  ```

- `src/loans/views.py:49 Mutant #44`

  ```diff
  @@ -46,7 +46,7 @@
           return redirect(f'/ui/loans/{loan.id}/')
       template = (
           'loans/loan-form.html'
  -        if request.method == 'POST' and request.headers.get('HX-Request') == 'true'
  +        if request.method == 'POST' or request.headers.get('HX-Request') == 'true'
           else 'loans/new.html'
       )
       return render(request, template, {'form': form})
  ```

- `src/loans/views.py:50 Mutant #45`

  ```diff
  @@ -47,7 +47,7 @@
       template = (
           'loans/loan-form.html'
           if request.method == 'POST' and request.headers.get('HX-Request') == 'true'
  -        else 'loans/new.html'
  +        else 'XXloans/new.htmlXX'
       )
       return render(request, template, {'form': form})
  ```

- `src/loans/views.py:51 Mutant #46`

  ```diff
  @@ -44,11 +44,7 @@
           if request.headers.get('HX-Request') == 'true':
               return render(request, 'loans/loan-created.html', {'loan': loan})
           return redirect(f'/ui/loans/{loan.id}/')
  -    template = (
  -        'loans/loan-form.html'
  -        if request.method == 'POST' and request.headers.get('HX-Request') == 'true'
  -        else 'loans/new.html'
  -    )
  +    template = None
       return render(request, template, {'form': form})
  ```

- `src/loans/views.py:52 Mutant #47`

  ```diff
  @@ -49,7 +49,7 @@
           if request.method == 'POST' and request.headers.get('HX-Request') == 'true'
           else 'loans/new.html'
       )
  -    return render(request, template, {'form': form})
  +    return render(request, template, {'XXformXX': form})
   def loan_detail(request, loan_id):
  ```

- `src/loans/views.py:56 Mutant #48`

  ```diff
  @@ -53,7 +53,7 @@
   def loan_detail(request, loan_id):
  -    body = loan_application.get_loan_text(loan_id)
  +    body = None
       if body is None:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       return HttpResponse(body, content_type='text/plain')
  ```

- `src/loans/views.py:57 Mutant #49`

  ```diff
  @@ -54,7 +54,7 @@
   def loan_detail(request, loan_id):
       body = loan_application.get_loan_text(loan_id)
  -    if body is None:
  +    if body is not None:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       return HttpResponse(body, content_type='text/plain')
  ```

- `src/loans/views.py:58 Mutant #50`

  ```diff
  @@ -55,7 +55,7 @@
   def loan_detail(request, loan_id):
       body = loan_application.get_loan_text(loan_id)
       if body is None:
  -        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  +        return HttpResponse('XXno such loan\nXX', status=404, content_type='text/plain')
       return HttpResponse(body, content_type='text/plain')
  ```

- `src/loans/views.py:58 Mutant #51`

  ```diff
  @@ -55,7 +55,7 @@
   def loan_detail(request, loan_id):
       body = loan_application.get_loan_text(loan_id)
       if body is None:
  -        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  +        return HttpResponse('no such loan\n', status=405, content_type='text/plain')
       return HttpResponse(body, content_type='text/plain')
  ```

- `src/loans/views.py:58 Mutant #52`

  ```diff
  @@ -55,7 +55,7 @@
   def loan_detail(request, loan_id):
       body = loan_application.get_loan_text(loan_id)
       if body is None:
  -        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  +        return HttpResponse('no such loan\n', status=404, content_type='XXtext/plainXX')
       return HttpResponse(body, content_type='text/plain')
  ```

- `src/loans/views.py:59 Mutant #53`

  ```diff
  @@ -56,7 +56,7 @@
       body = loan_application.get_loan_text(loan_id)
       if body is None:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  -    return HttpResponse(body, content_type='text/plain')
  +    return HttpResponse(body, content_type='XXtext/plainXX')
   @require_POST
  ```

- `src/loans/views.py:62 Mutant #54`

  ```diff
  @@ -58,8 +58,6 @@
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       return HttpResponse(body, content_type='text/plain')
  -
  -@require_POST
   def loan_return(request, loan_id):
       loan, updated = loan_application.return_loan(loan_id)
       if loan is None:
  ```

- `src/loans/views.py:66 Mutant #57`

  ```diff
  @@ -63,7 +63,7 @@
   def loan_return(request, loan_id):
       loan, updated = loan_application.return_loan(loan_id)
       if loan is None:
  -        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  +        return HttpResponse('XXno such loan\nXX', status=404, content_type='text/plain')
       if not updated:
           return HttpResponse('already returned\n', status=409, content_type='text/plain')
       return HttpResponse(loan_line(loan), content_type='text/plain')
  ```

- `src/loans/views.py:66 Mutant #58`

  ```diff
  @@ -63,7 +63,7 @@
   def loan_return(request, loan_id):
       loan, updated = loan_application.return_loan(loan_id)
       if loan is None:
  -        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  +        return HttpResponse('no such loan\n', status=405, content_type='text/plain')
       if not updated:
           return HttpResponse('already returned\n', status=409, content_type='text/plain')
       return HttpResponse(loan_line(loan), content_type='text/plain')
  ```

- `src/loans/views.py:66 Mutant #59`

  ```diff
  @@ -63,7 +63,7 @@
   def loan_return(request, loan_id):
       loan, updated = loan_application.return_loan(loan_id)
       if loan is None:
  -        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  +        return HttpResponse('no such loan\n', status=404, content_type='XXtext/plainXX')
       if not updated:
           return HttpResponse('already returned\n', status=409, content_type='text/plain')
       return HttpResponse(loan_line(loan), content_type='text/plain')
  ```

- `src/loans/views.py:68 Mutant #61`

  ```diff
  @@ -65,7 +65,7 @@
       if loan is None:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       if not updated:
  -        return HttpResponse('already returned\n', status=409, content_type='text/plain')
  +        return HttpResponse('XXalready returned\nXX', status=409, content_type='text/plain')
       return HttpResponse(loan_line(loan), content_type='text/plain')
  ```

- `src/loans/views.py:68 Mutant #62`

  ```diff
  @@ -65,7 +65,7 @@
       if loan is None:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       if not updated:
  -        return HttpResponse('already returned\n', status=409, content_type='text/plain')
  +        return HttpResponse('already returned\n', status=410, content_type='text/plain')
       return HttpResponse(loan_line(loan), content_type='text/plain')
  ```

- `src/loans/views.py:68 Mutant #63`

  ```diff
  @@ -65,7 +65,7 @@
       if loan is None:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       if not updated:
  -        return HttpResponse('already returned\n', status=409, content_type='text/plain')
  +        return HttpResponse('already returned\n', status=409, content_type='XXtext/plainXX')
       return HttpResponse(loan_line(loan), content_type='text/plain')
  ```

- `src/loans/views.py:69 Mutant #64`

  ```diff
  @@ -66,7 +66,7 @@
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       if not updated:
           return HttpResponse('already returned\n', status=409, content_type='text/plain')
  -    return HttpResponse(loan_line(loan), content_type='text/plain')
  +    return HttpResponse(loan_line(loan), content_type='XXtext/plainXX')
   @require_POST
  ```

- `src/loans/views.py:72 Mutant #65`

  ```diff
  @@ -68,8 +68,6 @@
           return HttpResponse('already returned\n', status=409, content_type='text/plain')
       return HttpResponse(loan_line(loan), content_type='text/plain')
  -
  -@require_POST
   def loan_return_page(request, loan_id):
       loan, updated = loan_application.return_loan(loan_id)
       if loan is None:
  ```

- `src/loans/views.py:74 Mutant #66`

  ```diff
  @@ -71,7 +71,7 @@
   @require_POST
   def loan_return_page(request, loan_id):
  -    loan, updated = loan_application.return_loan(loan_id)
  +    loan, updated = None
       if loan is None:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  ```

- `src/loans/views.py:75 Mutant #67`

  ```diff
  @@ -72,7 +72,7 @@
   @require_POST
   def loan_return_page(request, loan_id):
       loan, updated = loan_application.return_loan(loan_id)
  -    if loan is None:
  +    if loan is not None:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       if request.headers.get('HX-Request') == 'true':
  ```

- `src/loans/views.py:76 Mutant #68`

  ```diff
  @@ -73,7 +73,7 @@
   def loan_return_page(request, loan_id):
       loan, updated = loan_application.return_loan(loan_id)
       if loan is None:
  -        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  +        return HttpResponse('XXno such loan\nXX', status=404, content_type='text/plain')
       if request.headers.get('HX-Request') == 'true':
           return render(
  ```

- `src/loans/views.py:76 Mutant #69`

  ```diff
  @@ -73,7 +73,7 @@
   def loan_return_page(request, loan_id):
       loan, updated = loan_application.return_loan(loan_id)
       if loan is None:
  -        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  +        return HttpResponse('no such loan\n', status=405, content_type='text/plain')
       if request.headers.get('HX-Request') == 'true':
           return render(
  ```

- `src/loans/views.py:76 Mutant #70`

  ```diff
  @@ -73,7 +73,7 @@
   def loan_return_page(request, loan_id):
       loan, updated = loan_application.return_loan(loan_id)
       if loan is None:
  -        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  +        return HttpResponse('no such loan\n', status=404, content_type='XXtext/plainXX')
       if request.headers.get('HX-Request') == 'true':
           return render(
  ```

- `src/loans/views.py:78 Mutant #71`

  ```diff
  @@ -75,7 +75,7 @@
       if loan is None:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  -    if request.headers.get('HX-Request') == 'true':
  +    if request.headers.get('XXHX-RequestXX') == 'true':
           return render(
               request,
               'loans/return-status.html',
  ```

- `src/loans/views.py:78 Mutant #72`

  ```diff
  @@ -75,7 +75,7 @@
       if loan is None:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  -    if request.headers.get('HX-Request') == 'true':
  +    if request.headers.get('HX-Request') != 'true':
           return render(
               request,
               'loans/return-status.html',
  ```

- `src/loans/views.py:78 Mutant #73`

  ```diff
  @@ -75,7 +75,7 @@
       if loan is None:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  -    if request.headers.get('HX-Request') == 'true':
  +    if request.headers.get('HX-Request') == 'XXtrueXX':
           return render(
               request,
               'loans/return-status.html',
  ```

- `src/loans/views.py:81 Mutant #74`

  ```diff
  @@ -78,7 +78,7 @@
       if request.headers.get('HX-Request') == 'true':
           return render(
               request,
  -            'loans/return-status.html',
  +            'XXloans/return-status.htmlXX',
               {'loan': loan, 'updated': updated},
           )
       if not updated:
  ```

- `src/loans/views.py:82 Mutant #75`

  ```diff
  @@ -79,7 +79,7 @@
           return render(
               request,
               'loans/return-status.html',
  -            {'loan': loan, 'updated': updated},
  +            {'XXloanXX': loan, 'updated': updated},
           )
       if not updated:
           return render(
  ```

- `src/loans/views.py:82 Mutant #76`

  ```diff
  @@ -79,7 +79,7 @@
           return render(
               request,
               'loans/return-status.html',
  -            {'loan': loan, 'updated': updated},
  +            {'loan': loan, 'XXupdatedXX': updated},
           )
       if not updated:
           return render(
  ```

- `src/loans/views.py:84 Mutant #77`

  ```diff
  @@ -81,7 +81,7 @@
               'loans/return-status.html',
               {'loan': loan, 'updated': updated},
           )
  -    if not updated:
  +    if  updated:
           return render(
               request,
               'loans/detail.html',
  ```

- `src/loans/views.py:87 Mutant #78`

  ```diff
  @@ -84,7 +84,7 @@
       if not updated:
           return render(
               request,
  -            'loans/detail.html',
  +            'XXloans/detail.htmlXX',
               {'loan': loan, 'return_error': True},
               status=409,
           )
  ```

- `src/loans/views.py:88 Mutant #79`

  ```diff
  @@ -85,7 +85,7 @@
           return render(
               request,
               'loans/detail.html',
  -            {'loan': loan, 'return_error': True},
  +            {'XXloanXX': loan, 'return_error': True},
               status=409,
           )
       return redirect(f'/ui/loans/{loan.id}/')
  ```

- `src/loans/views.py:88 Mutant #80`

  ```diff
  @@ -85,7 +85,7 @@
           return render(
               request,
               'loans/detail.html',
  -            {'loan': loan, 'return_error': True},
  +            {'loan': loan, 'XXreturn_errorXX': True},
               status=409,
           )
       return redirect(f'/ui/loans/{loan.id}/')
  ```

- `src/loans/views.py:88 Mutant #81`

  ```diff
  @@ -85,7 +85,7 @@
           return render(
               request,
               'loans/detail.html',
  -            {'loan': loan, 'return_error': True},
  +            {'loan': loan, 'return_error': False},
               status=409,
           )
       return redirect(f'/ui/loans/{loan.id}/')
  ```

- `src/loans/views.py:89 Mutant #82`

  ```diff
  @@ -86,7 +86,7 @@
               request,
               'loans/detail.html',
               {'loan': loan, 'return_error': True},
  -            status=409,
  +            status=410,
           )
       return redirect(f'/ui/loans/{loan.id}/')
  ```

- `src/loans/views.py:91 Mutant #83`

  ```diff
  @@ -88,5 +88,5 @@
               {'loan': loan, 'return_error': True},
               status=409,
           )
  -    return redirect(f'/ui/loans/{loan.id}/')
  +    return redirect(f'XX/ui/loans/{loan.id}/XX')
  ```

- `src/holds/views.py:23 Mutant #104`

  ```diff
  @@ -19,8 +19,6 @@
       status, message = FAILURE_RESPONSES[failure.code]
       return HttpResponse(f'{message}\n', status=status, content_type='text/plain')
  -
  -@require_http_methods(['GET', 'POST'])
   def hold_collection(request):
       if request.method == 'GET':
           return HttpResponse(
  ```

- `src/holds/views.py:40 Mutant #116`

  ```diff
  @@ -36,8 +36,6 @@
           return _failure_response(result)
       return HttpResponse(hold_line(result), status=201, content_type='text/plain')
  -
  -@require_POST
   def hold_cancel(request, hold_id):
       result = hold_application.cancel(hold_id)
       if isinstance(result, HoldFailure):
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

- `src/reports/management/commands/monthly_report.py:14 Mutant #121`

  ```diff
  @@ -11,7 +11,7 @@
       help = 'Produce the previous month lending report.'
       def handle(self, *args, **options):
  -        reports = monthly_report.for_previous_month(timezone.localdate())
  +        reports = None
           output = StringIO(newline='')
           writer = csv.writer(output, lineterminator='\n')
           writer.writerow(['member_id', 'loans_started', 'late_returns', 'total_late_fees_cents'])
  ```

- `src/reports/management/commands/monthly_report.py:15 Mutant #122`

  ```diff
  @@ -12,7 +12,7 @@
       def handle(self, *args, **options):
           reports = monthly_report.for_previous_month(timezone.localdate())
  -        output = StringIO(newline='')
  +        output = StringIO(newline='XXXX')
           writer = csv.writer(output, lineterminator='\n')
           writer.writerow(['member_id', 'loans_started', 'late_returns', 'total_late_fees_cents'])
           for report in reports:
  ```

- `src/reports/management/commands/monthly_report.py:15 Mutant #123`

  ```diff
  @@ -12,7 +12,7 @@
       def handle(self, *args, **options):
           reports = monthly_report.for_previous_month(timezone.localdate())
  -        output = StringIO(newline='')
  +        output = None
           writer = csv.writer(output, lineterminator='\n')
           writer.writerow(['member_id', 'loans_started', 'late_returns', 'total_late_fees_cents'])
           for report in reports:
  ```

- `src/reports/management/commands/monthly_report.py:16 Mutant #124`

  ```diff
  @@ -13,7 +13,7 @@
       def handle(self, *args, **options):
           reports = monthly_report.for_previous_month(timezone.localdate())
           output = StringIO(newline='')
  -        writer = csv.writer(output, lineterminator='\n')
  +        writer = csv.writer(output, lineterminator='XX\nXX')
           writer.writerow(['member_id', 'loans_started', 'late_returns', 'total_late_fees_cents'])
           for report in reports:
               writer.writerow(
  ```

- `src/reports/management/commands/monthly_report.py:16 Mutant #125`

  ```diff
  @@ -13,7 +13,7 @@
       def handle(self, *args, **options):
           reports = monthly_report.for_previous_month(timezone.localdate())
           output = StringIO(newline='')
  -        writer = csv.writer(output, lineterminator='\n')
  +        writer = None
           writer.writerow(['member_id', 'loans_started', 'late_returns', 'total_late_fees_cents'])
           for report in reports:
               writer.writerow(
  ```

- `src/reports/management/commands/monthly_report.py:17 Mutant #126`

  ```diff
  @@ -14,7 +14,7 @@
           reports = monthly_report.for_previous_month(timezone.localdate())
           output = StringIO(newline='')
           writer = csv.writer(output, lineterminator='\n')
  -        writer.writerow(['member_id', 'loans_started', 'late_returns', 'total_late_fees_cents'])
  +        writer.writerow(['XXmember_idXX', 'loans_started', 'late_returns', 'total_late_fees_cents'])
           for report in reports:
               writer.writerow(
                   [
  ```

- `src/reports/management/commands/monthly_report.py:17 Mutant #127`

  ```diff
  @@ -14,7 +14,7 @@
           reports = monthly_report.for_previous_month(timezone.localdate())
           output = StringIO(newline='')
           writer = csv.writer(output, lineterminator='\n')
  -        writer.writerow(['member_id', 'loans_started', 'late_returns', 'total_late_fees_cents'])
  +        writer.writerow(['member_id', 'XXloans_startedXX', 'late_returns', 'total_late_fees_cents'])
           for report in reports:
               writer.writerow(
                   [
  ```

- `src/reports/management/commands/monthly_report.py:17 Mutant #128`

  ```diff
  @@ -14,7 +14,7 @@
           reports = monthly_report.for_previous_month(timezone.localdate())
           output = StringIO(newline='')
           writer = csv.writer(output, lineterminator='\n')
  -        writer.writerow(['member_id', 'loans_started', 'late_returns', 'total_late_fees_cents'])
  +        writer.writerow(['member_id', 'loans_started', 'XXlate_returnsXX', 'total_late_fees_cents'])
           for report in reports:
               writer.writerow(
                   [
  ```

- `src/reports/management/commands/monthly_report.py:17 Mutant #129`

  ```diff
  @@ -14,7 +14,7 @@
           reports = monthly_report.for_previous_month(timezone.localdate())
           output = StringIO(newline='')
           writer = csv.writer(output, lineterminator='\n')
  -        writer.writerow(['member_id', 'loans_started', 'late_returns', 'total_late_fees_cents'])
  +        writer.writerow(['member_id', 'loans_started', 'late_returns', 'XXtotal_late_fees_centsXX'])
           for report in reports:
               writer.writerow(
                   [
  ```

- `src/reports/management/commands/monthly_report.py:27 Mutant #130`

  ```diff
  @@ -24,5 +24,5 @@
                       report.total_late_fees_cents,
                   ]
               )
  -        self.stdout.write(output.getvalue(), ending='')
  +        self.stdout.write(output.getvalue(), ending='XXXX')
  ```

- `src/loans/models.py:7 Mutant #131`

  ```diff
  @@ -4,7 +4,7 @@
   class Loan(models.Model):
  -    id = models.CharField(max_length=255, primary_key=True)
  +    id = models.CharField(max_length=256, primary_key=True)
       member = models.CharField(max_length=255)
       isbn = models.CharField(max_length=255)
       lent_on = models.DateField()
  ```

- `src/loans/models.py:8 Mutant #134`

  ```diff
  @@ -5,7 +5,7 @@
   class Loan(models.Model):
       id = models.CharField(max_length=255, primary_key=True)
  -    member = models.CharField(max_length=255)
  +    member = models.CharField(max_length=256)
       isbn = models.CharField(max_length=255)
       lent_on = models.DateField()
       returned_on = models.DateField(null=True, blank=True)
  ```

- `src/loans/models.py:9 Mutant #136`

  ```diff
  @@ -6,7 +6,7 @@
   class Loan(models.Model):
       id = models.CharField(max_length=255, primary_key=True)
       member = models.CharField(max_length=255)
  -    isbn = models.CharField(max_length=255)
  +    isbn = models.CharField(max_length=256)
       lent_on = models.DateField()
       returned_on = models.DateField(null=True, blank=True)
  ```

- `src/loans/models.py:11 Mutant #139`

  ```diff
  @@ -8,7 +8,7 @@
       member = models.CharField(max_length=255)
       isbn = models.CharField(max_length=255)
       lent_on = models.DateField()
  -    returned_on = models.DateField(null=True, blank=True)
  +    returned_on = models.DateField(null=False, blank=True)
       class Meta:
           ordering = ('id',)
  ```

- `src/loans/models.py:11 Mutant #140`

  ```diff
  @@ -8,7 +8,7 @@
       member = models.CharField(max_length=255)
       isbn = models.CharField(max_length=255)
       lent_on = models.DateField()
  -    returned_on = models.DateField(null=True, blank=True)
  +    returned_on = models.DateField(null=True, blank=False)
       class Meta:
           ordering = ('id',)
  ```

- `src/loans/models.py:14 Mutant #143`

  ```diff
  @@ -11,7 +11,7 @@
       returned_on = models.DateField(null=True, blank=True)
       class Meta:
  -        ordering = ('id',)
  +        ordering = None
       @property
       def due_on(self):
  ```

- `src/fees/urls.py:9 Mutant #150`

  ```diff
  @@ -6,6 +6,6 @@
       path('fees/<str:loan_id>', views.fee_detail),
       path('payments/<str:loan_id>', views.payment),
       path('ui/fees/<str:loan_id>/', views.fee_page),
  -    path('ui/payments/<str:loan_id>/', views.payment_page),
  +    path('XXui/payments/<str:loan_id>/XX', views.payment_page),
   ]
  ```

- `src/library_info/urls.py:6 Mutant #156`

  ```diff
  @@ -3,7 +3,7 @@
   from . import views
   urlpatterns = [
  -    path('about', views.about),
  +    path('XXaboutXX', views.about),
       path('ui/about/', views.about_page),
   ]
  ```

- `src/library_info/urls.py:7 Mutant #157`

  ```diff
  @@ -4,6 +4,6 @@
   urlpatterns = [
       path('about', views.about),
  -    path('ui/about/', views.about_page),
  +    path('XXui/about/XX', views.about_page),
   ]
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

- `src/loans/services.py:58 Mutant #5`

  ```diff
  @@ -55,7 +55,7 @@
           return self.repository.mark_returned(loan_id, self.clock.today())
       def list_loans_text(self) -> str:
  -        return ''.join(loan_line(loan) for loan in self.repository.all())
  +        return 'XXXX'.join(loan_line(loan) for loan in self.repository.all())
       def get_loan_text(self, loan_id: str) -> str | None:
           loan = self.repository.find(loan_id)
  ```

- `src/loans/services.py:61 Mutant #6`

  ```diff
  @@ -58,7 +58,7 @@
           return ''.join(loan_line(loan) for loan in self.repository.all())
       def get_loan_text(self, loan_id: str) -> str | None:
  -        loan = self.repository.find(loan_id)
  +        loan = None
           return loan_line(loan) if loan else None
       def active_loan_for_isbn(self, isbn: str) -> ActiveLoan | None:
  ```

- `src/loans/services.py:71 Mutant #12`

  ```diff
  @@ -68,7 +68,7 @@
   def loan_line(loan):
       output = StringIO(newline='')
  -    writer = csv.writer(output, delimiter=';', lineterminator='\n')
  +    writer = csv.writer(output, delimiter=';', lineterminator='XX\nXX')
       writer.writerow(
           [
               loan.id,
  ```

- `src/loans/services.py:79 Mutant #14`

  ```diff
  @@ -76,7 +76,7 @@
               loan.isbn,
               loan.lent_on.isoformat(),
               loan.due_on.isoformat(),
  -            loan.returned_on.isoformat() if loan.returned_on else '',
  +            loan.returned_on.isoformat() if loan.returned_on else 'XXXX',
           ]
       )
       return output.getvalue()
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

- `src/holds/repository.py:10 Mutant #16`

  ```diff
  @@ -7,7 +7,7 @@
   from .models import Hold
   from .services import HoldIdentity
  -_HOLD_PLACEMENT_LOCK = 0x484F4C44
  +_HOLD_PLACEMENT_LOCK = None
   class DjangoHoldRepository:
  ```

- `src/holds/repository.py:37 Mutant #28`

  ```diff
  @@ -34,7 +34,7 @@
           return self.active(isbn, today).filter(member=member).exists()
       def next_identity(self):
  -        sequence = (Hold.objects.aggregate(maximum=Max('sequence'))['maximum'] or 0) + 1
  +        sequence = (Hold.objects.aggregate(maximum=Max('sequence'))['maximum'] or 1) + 1
           return HoldIdentity(f'H{sequence}', sequence)
       @transaction.atomic
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

- `src/holds/repository.py:53 Mutant #35`

  ```diff
  @@ -50,7 +50,6 @@
       def find(self, hold_id):
           return Hold.objects.filter(pk=hold_id).first()
  -    @transaction.atomic
       def cancel(self, hold_id, cancelled_on):
           hold = Hold.objects.select_for_update().get(pk=hold_id)
           hold.cancelled_on = cancelled_on
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

- `src/loans/urls.py:8 Mutant #82`

  ```diff
  @@ -5,7 +5,7 @@
   urlpatterns = [
       path('loans', views.loan_collection),
       path('loans/<str:loan_id>/return', views.loan_return),
  -    path('loans/<str:loan_id>', views.loan_detail),
  +    path('XXloans/<str:loan_id>XX', views.loan_detail),
       path('ui/loans/', views.loan_catalog),
       path('ui/loans/new/', views.loan_lend_page),
       path('ui/loans/<str:loan_id>/return/', views.loan_return_page),
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

- `src/loans/urls.py:10 Mutant #84`

  ```diff
  @@ -7,7 +7,7 @@
       path('loans/<str:loan_id>/return', views.loan_return),
       path('loans/<str:loan_id>', views.loan_detail),
       path('ui/loans/', views.loan_catalog),
  -    path('ui/loans/new/', views.loan_lend_page),
  +    path('XXui/loans/new/XX', views.loan_lend_page),
       path('ui/loans/<str:loan_id>/return/', views.loan_return_page),
       path('ui/loans/<str:loan_id>/', views.loan_catalog_detail),
   ]
  ```

- `src/loans/urls.py:11 Mutant #85`

  ```diff
  @@ -8,7 +8,7 @@
       path('loans/<str:loan_id>', views.loan_detail),
       path('ui/loans/', views.loan_catalog),
       path('ui/loans/new/', views.loan_lend_page),
  -    path('ui/loans/<str:loan_id>/return/', views.loan_return_page),
  +    path('XXui/loans/<str:loan_id>/return/XX', views.loan_return_page),
       path('ui/loans/<str:loan_id>/', views.loan_catalog_detail),
   ]
  ```

- `src/loans/urls.py:12 Mutant #86`

  ```diff
  @@ -9,6 +9,6 @@
       path('ui/loans/', views.loan_catalog),
       path('ui/loans/new/', views.loan_lend_page),
       path('ui/loans/<str:loan_id>/return/', views.loan_return_page),
  -    path('ui/loans/<str:loan_id>/', views.loan_catalog_detail),
  +    path('XXui/loans/<str:loan_id>/XX', views.loan_catalog_detail),
   ]
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

- `src/reports/services.py:27 Mutant #2`

  ```diff
  @@ -23,8 +23,6 @@
   class MonthlyReportRepository(Protocol):
       def started_between(self, start: date, end: date) -> Iterable[LoanRecord]: ...
  -
  -@dataclass(frozen=True)
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

- `src/reports/services.py:37 Mutant #4`

  ```diff
  @@ -34,7 +34,7 @@
   @dataclass
   class _MemberTotals:
  -    loans_started: int = 0
  +    loans_started: int = 1
       late_returns: int = 0
       total_late_fees_cents: int = 0
  ```

- `src/reports/services.py:37 Mutant #5`

  ```diff
  @@ -34,7 +34,7 @@
   @dataclass
   class _MemberTotals:
  -    loans_started: int = 0
  +    loans_started: int = None
       late_returns: int = 0
       total_late_fees_cents: int = 0
  ```

- `src/reports/services.py:38 Mutant #6`

  ```diff
  @@ -35,7 +35,7 @@
   @dataclass
   class _MemberTotals:
       loans_started: int = 0
  -    late_returns: int = 0
  +    late_returns: int = 1
       total_late_fees_cents: int = 0
  ```

- `src/reports/services.py:38 Mutant #7`

  ```diff
  @@ -35,7 +35,7 @@
   @dataclass
   class _MemberTotals:
       loans_started: int = 0
  -    late_returns: int = 0
  +    late_returns: int = None
       total_late_fees_cents: int = 0
  ```

- `src/reports/services.py:39 Mutant #8`

  ```diff
  @@ -36,7 +36,7 @@
   class _MemberTotals:
       loans_started: int = 0
       late_returns: int = 0
  -    total_late_fees_cents: int = 0
  +    total_late_fees_cents: int = 1
   class MonthlyReportApplication:
  ```

- `src/reports/services.py:39 Mutant #9`

  ```diff
  @@ -36,7 +36,7 @@
   class _MemberTotals:
       loans_started: int = 0
       late_returns: int = 0
  -    total_late_fees_cents: int = 0
  +    total_late_fees_cents: int = None
   class MonthlyReportApplication:
  ```

- `src/reports/services.py:44 Mutant #10`

  ```diff
  @@ -41,7 +41,7 @@
   class MonthlyReportApplication:
       def __init__(self, loans: MonthlyReportRepository, fees: FeeCalculator):
  -        self.loans = loans
  +        self.loans = None
           self.fees = fees
       def for_previous_month(self, as_of: date) -> list[MemberMonthlyReport]:
  ```

- `src/reports/services.py:45 Mutant #11`

  ```diff
  @@ -42,7 +42,7 @@
   class MonthlyReportApplication:
       def __init__(self, loans: MonthlyReportRepository, fees: FeeCalculator):
           self.loans = loans
  -        self.fees = fees
  +        self.fees = None
       def for_previous_month(self, as_of: date) -> list[MemberMonthlyReport]:
           end = as_of.replace(day=1)
  ```

- `src/reports/services.py:48 Mutant #12`

  ```diff
  @@ -45,7 +45,7 @@
           self.fees = fees
       def for_previous_month(self, as_of: date) -> list[MemberMonthlyReport]:
  -        end = as_of.replace(day=1)
  +        end = as_of.replace(day=2)
           start = (end - timedelta(days=1)).replace(day=1)
           totals: dict[str, _MemberTotals] = defaultdict(_MemberTotals)
  ```

- `src/reports/services.py:48 Mutant #13`

  ```diff
  @@ -45,7 +45,7 @@
           self.fees = fees
       def for_previous_month(self, as_of: date) -> list[MemberMonthlyReport]:
  -        end = as_of.replace(day=1)
  +        end = None
           start = (end - timedelta(days=1)).replace(day=1)
           totals: dict[str, _MemberTotals] = defaultdict(_MemberTotals)
  ```

- `src/reports/services.py:49 Mutant #14`

  ```diff
  @@ -46,7 +46,7 @@
       def for_previous_month(self, as_of: date) -> list[MemberMonthlyReport]:
           end = as_of.replace(day=1)
  -        start = (end - timedelta(days=1)).replace(day=1)
  +        start = (end + timedelta(days=1)).replace(day=1)
           totals: dict[str, _MemberTotals] = defaultdict(_MemberTotals)
           for loan in self.loans.started_between(start, end):
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

- `src/reports/services.py:49 Mutant #16`

  ```diff
  @@ -46,7 +46,7 @@
       def for_previous_month(self, as_of: date) -> list[MemberMonthlyReport]:
           end = as_of.replace(day=1)
  -        start = (end - timedelta(days=1)).replace(day=1)
  +        start = (end - timedelta(days=1)).replace(day=2)
           totals: dict[str, _MemberTotals] = defaultdict(_MemberTotals)
           for loan in self.loans.started_between(start, end):
  ```

- `src/reports/services.py:49 Mutant #17`

  ```diff
  @@ -46,7 +46,7 @@
       def for_previous_month(self, as_of: date) -> list[MemberMonthlyReport]:
           end = as_of.replace(day=1)
  -        start = (end - timedelta(days=1)).replace(day=1)
  +        start = None
           totals: dict[str, _MemberTotals] = defaultdict(_MemberTotals)
           for loan in self.loans.started_between(start, end):
  ```

- `src/reports/services.py:50 Mutant #18`

  ```diff
  @@ -47,7 +47,7 @@
       def for_previous_month(self, as_of: date) -> list[MemberMonthlyReport]:
           end = as_of.replace(day=1)
           start = (end - timedelta(days=1)).replace(day=1)
  -        totals: dict[str, _MemberTotals] = defaultdict(_MemberTotals)
  +        totals: dict[str, _MemberTotals] = None
           for loan in self.loans.started_between(start, end):
               member_totals = totals[loan.member]
  ```

- `src/reports/services.py:53 Mutant #19`

  ```diff
  @@ -50,7 +50,7 @@
           totals: dict[str, _MemberTotals] = defaultdict(_MemberTotals)
           for loan in self.loans.started_between(start, end):
  -            member_totals = totals[loan.member]
  +            member_totals = None
               member_totals.loans_started += 1
               if loan.returned_on is not None and loan.returned_on > loan.due_on:
                   member_totals.late_returns += 1
  ```

- `src/reports/services.py:54 Mutant #20`

  ```diff
  @@ -51,7 +51,7 @@
           for loan in self.loans.started_between(start, end):
               member_totals = totals[loan.member]
  -            member_totals.loans_started += 1
  +            member_totals.loans_started = 1
               if loan.returned_on is not None and loan.returned_on > loan.due_on:
                   member_totals.late_returns += 1
  ```

- `src/reports/services.py:54 Mutant #21`

  ```diff
  @@ -51,7 +51,7 @@
           for loan in self.loans.started_between(start, end):
               member_totals = totals[loan.member]
  -            member_totals.loans_started += 1
  +            member_totals.loans_started -= 1
               if loan.returned_on is not None and loan.returned_on > loan.due_on:
                   member_totals.late_returns += 1
  ```

- `src/reports/services.py:54 Mutant #22`

  ```diff
  @@ -51,7 +51,7 @@
           for loan in self.loans.started_between(start, end):
               member_totals = totals[loan.member]
  -            member_totals.loans_started += 1
  +            member_totals.loans_started += 2
               if loan.returned_on is not None and loan.returned_on > loan.due_on:
                   member_totals.late_returns += 1
  ```

- `src/reports/services.py:55 Mutant #23`

  ```diff
  @@ -52,7 +52,7 @@
           for loan in self.loans.started_between(start, end):
               member_totals = totals[loan.member]
               member_totals.loans_started += 1
  -            if loan.returned_on is not None and loan.returned_on > loan.due_on:
  +            if loan.returned_on is  None and loan.returned_on > loan.due_on:
                   member_totals.late_returns += 1
               fee = self.fees.fee_for(loan.id)
  ```

- `src/reports/services.py:55 Mutant #24`

  ```diff
  @@ -52,7 +52,7 @@
           for loan in self.loans.started_between(start, end):
               member_totals = totals[loan.member]
               member_totals.loans_started += 1
  -            if loan.returned_on is not None and loan.returned_on > loan.due_on:
  +            if loan.returned_on is not None and loan.returned_on >= loan.due_on:
                   member_totals.late_returns += 1
               fee = self.fees.fee_for(loan.id)
  ```

- `src/reports/services.py:55 Mutant #25`

  ```diff
  @@ -52,7 +52,7 @@
           for loan in self.loans.started_between(start, end):
               member_totals = totals[loan.member]
               member_totals.loans_started += 1
  -            if loan.returned_on is not None and loan.returned_on > loan.due_on:
  +            if loan.returned_on is not None or loan.returned_on > loan.due_on:
                   member_totals.late_returns += 1
               fee = self.fees.fee_for(loan.id)
  ```

- `src/reports/services.py:56 Mutant #26`

  ```diff
  @@ -53,7 +53,7 @@
               member_totals = totals[loan.member]
               member_totals.loans_started += 1
               if loan.returned_on is not None and loan.returned_on > loan.due_on:
  -                member_totals.late_returns += 1
  +                member_totals.late_returns = 1
               fee = self.fees.fee_for(loan.id)
               if fee is not None:
  ```

- `src/reports/services.py:56 Mutant #27`

  ```diff
  @@ -53,7 +53,7 @@
               member_totals = totals[loan.member]
               member_totals.loans_started += 1
               if loan.returned_on is not None and loan.returned_on > loan.due_on:
  -                member_totals.late_returns += 1
  +                member_totals.late_returns -= 1
               fee = self.fees.fee_for(loan.id)
               if fee is not None:
  ```

- `src/reports/services.py:56 Mutant #28`

  ```diff
  @@ -53,7 +53,7 @@
               member_totals = totals[loan.member]
               member_totals.loans_started += 1
               if loan.returned_on is not None and loan.returned_on > loan.due_on:
  -                member_totals.late_returns += 1
  +                member_totals.late_returns += 2
               fee = self.fees.fee_for(loan.id)
               if fee is not None:
  ```

- `src/reports/services.py:58 Mutant #29`

  ```diff
  @@ -55,7 +55,7 @@
               if loan.returned_on is not None and loan.returned_on > loan.due_on:
                   member_totals.late_returns += 1
  -            fee = self.fees.fee_for(loan.id)
  +            fee = None
               if fee is not None:
                   member_totals.total_late_fees_cents += fee.amount_cents
  ```

- `src/reports/services.py:59 Mutant #30`

  ```diff
  @@ -56,7 +56,7 @@
                   member_totals.late_returns += 1
               fee = self.fees.fee_for(loan.id)
  -            if fee is not None:
  +            if fee is  None:
                   member_totals.total_late_fees_cents += fee.amount_cents
           return sorted(
  ```

- `src/reports/services.py:60 Mutant #31`

  ```diff
  @@ -57,7 +57,7 @@
               fee = self.fees.fee_for(loan.id)
               if fee is not None:
  -                member_totals.total_late_fees_cents += fee.amount_cents
  +                member_totals.total_late_fees_cents = fee.amount_cents
           return sorted(
               (
  ```

- `src/reports/services.py:60 Mutant #32`

  ```diff
  @@ -57,7 +57,7 @@
               fee = self.fees.fee_for(loan.id)
               if fee is not None:
  -                member_totals.total_late_fees_cents += fee.amount_cents
  +                member_totals.total_late_fees_cents -= fee.amount_cents
           return sorted(
               (
  ```

- `src/reports/services.py:72 Mutant #33`

  ```diff
  @@ -69,6 +69,6 @@
                   )
                   for member_id, member_totals in totals.items()
               ),
  -            key=lambda report: (-report.total_late_fees_cents, report.member_id),
  +            key=lambda report: (+report.total_late_fees_cents, report.member_id),
           )
  ```

- `src/reports/services.py:72 Mutant #34`

  ```diff
  @@ -69,6 +69,6 @@
                   )
                   for member_id, member_totals in totals.items()
               ),
  -            key=lambda report: (-report.total_late_fees_cents, report.member_id),
  +            key=lambda report: None,
           )
  ```

- `src/fees/views.py:11 Mutant #35`

  ```diff
  @@ -7,8 +7,6 @@
   from .composition import fee_application
   from .view_helpers import fee_or_404, format_fee_amount, gateway_result
  -
  -@require_GET
   def fee_detail(request, loan_id):
       fee = fee_or_404(loan_id)
       if isinstance(fee, HttpResponse):
  ```

- `src/fees/views.py:25 Mutant #42`

  ```diff
  @@ -21,8 +21,6 @@
       )
       return HttpResponse(body, content_type='text/html')
  -
  -@require_POST
   def payment(request, loan_id):
       body, status = gateway_result(loan_id)
       if status == 404:
  ```

- `src/fees/views.py:33 Mutant #50`

  ```diff
  @@ -29,8 +29,6 @@
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       return HttpResponse(body, status=status, content_type='text/plain')
  -
  -@require_GET
   def fee_page(request, loan_id):
       fee = fee_or_404(loan_id)
       if isinstance(fee, HttpResponse):
  ```

- `src/fees/views.py:46 Mutant #56`

  ```diff
  @@ -42,8 +42,6 @@
           {'loan_id': loan_id, 'fee': fee, 'amount': format_fee_amount(fee.amount_cents)},
       )
  -
  -@require_POST
   def payment_page(request, loan_id):
       body, status = gateway_result(loan_id)
       if status == 404:
  ```

- `src/fees/views.py:48 Mutant #57`

  ```diff
  @@ -45,7 +45,7 @@
   @require_POST
   def payment_page(request, loan_id):
  -    body, status = gateway_result(loan_id)
  +    body, status = None
       if status == 404:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  ```

- `src/fees/views.py:49 Mutant #58`

  ```diff
  @@ -46,7 +46,7 @@
   @require_POST
   def payment_page(request, loan_id):
       body, status = gateway_result(loan_id)
  -    if status == 404:
  +    if status != 404:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       context = {'body': body, 'success': status == 200}
  ```

- `src/fees/views.py:49 Mutant #59`

  ```diff
  @@ -46,7 +46,7 @@
   @require_POST
   def payment_page(request, loan_id):
       body, status = gateway_result(loan_id)
  -    if status == 404:
  +    if status == 405:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       context = {'body': body, 'success': status == 200}
  ```

- `src/fees/views.py:50 Mutant #60`

  ```diff
  @@ -47,7 +47,7 @@
   def payment_page(request, loan_id):
       body, status = gateway_result(loan_id)
       if status == 404:
  -        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  +        return HttpResponse('XXno such loan\nXX', status=404, content_type='text/plain')
       context = {'body': body, 'success': status == 200}
       if request.headers.get('HX-Request') == 'true':
  ```

- `src/fees/views.py:50 Mutant #61`

  ```diff
  @@ -47,7 +47,7 @@
   def payment_page(request, loan_id):
       body, status = gateway_result(loan_id)
       if status == 404:
  -        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  +        return HttpResponse('no such loan\n', status=405, content_type='text/plain')
       context = {'body': body, 'success': status == 200}
       if request.headers.get('HX-Request') == 'true':
  ```

- `src/fees/views.py:50 Mutant #62`

  ```diff
  @@ -47,7 +47,7 @@
   def payment_page(request, loan_id):
       body, status = gateway_result(loan_id)
       if status == 404:
  -        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  +        return HttpResponse('no such loan\n', status=404, content_type='XXtext/plainXX')
       context = {'body': body, 'success': status == 200}
       if request.headers.get('HX-Request') == 'true':
  ```

- `src/fees/views.py:52 Mutant #63`

  ```diff
  @@ -49,7 +49,7 @@
       if status == 404:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  -    context = {'body': body, 'success': status == 200}
  +    context = {'XXbodyXX': body, 'success': status == 200}
       if request.headers.get('HX-Request') == 'true':
           return render(
               request,
  ```

- `src/fees/views.py:52 Mutant #64`

  ```diff
  @@ -49,7 +49,7 @@
       if status == 404:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  -    context = {'body': body, 'success': status == 200}
  +    context = {'body': body, 'XXsuccessXX': status == 200}
       if request.headers.get('HX-Request') == 'true':
           return render(
               request,
  ```

- `src/fees/views.py:52 Mutant #65`

  ```diff
  @@ -49,7 +49,7 @@
       if status == 404:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  -    context = {'body': body, 'success': status == 200}
  +    context = {'body': body, 'success': status != 200}
       if request.headers.get('HX-Request') == 'true':
           return render(
               request,
  ```

- `src/fees/views.py:52 Mutant #66`

  ```diff
  @@ -49,7 +49,7 @@
       if status == 404:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  -    context = {'body': body, 'success': status == 200}
  +    context = {'body': body, 'success': status == 201}
       if request.headers.get('HX-Request') == 'true':
           return render(
               request,
  ```

- `src/fees/views.py:52 Mutant #67`

  ```diff
  @@ -49,7 +49,7 @@
       if status == 404:
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
  -    context = {'body': body, 'success': status == 200}
  +    context = None
       if request.headers.get('HX-Request') == 'true':
           return render(
               request,
  ```

- `src/fees/views.py:53 Mutant #68`

  ```diff
  @@ -50,7 +50,7 @@
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       context = {'body': body, 'success': status == 200}
  -    if request.headers.get('HX-Request') == 'true':
  +    if request.headers.get('XXHX-RequestXX') == 'true':
           return render(
               request,
               'fees/payment-status.html',
  ```

- `src/fees/views.py:53 Mutant #69`

  ```diff
  @@ -50,7 +50,7 @@
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       context = {'body': body, 'success': status == 200}
  -    if request.headers.get('HX-Request') == 'true':
  +    if request.headers.get('HX-Request') != 'true':
           return render(
               request,
               'fees/payment-status.html',
  ```

- `src/fees/views.py:53 Mutant #70`

  ```diff
  @@ -50,7 +50,7 @@
           return HttpResponse('no such loan\n', status=404, content_type='text/plain')
       context = {'body': body, 'success': status == 200}
  -    if request.headers.get('HX-Request') == 'true':
  +    if request.headers.get('HX-Request') == 'XXtrueXX':
           return render(
               request,
               'fees/payment-status.html',
  ```

- `src/fees/views.py:56 Mutant #71`

  ```diff
  @@ -53,7 +53,7 @@
       if request.headers.get('HX-Request') == 'true':
           return render(
               request,
  -            'fees/payment-status.html',
  +            'XXfees/payment-status.htmlXX',
               context,
               status=status,
           )
  ```

- `src/fees/views.py:61 Mutant #72`

  ```diff
  @@ -58,7 +58,7 @@
               status=status,
           )
  -    fee = fee_application.fee_for(loan_id)
  +    fee = None
       return render(
           request,
           'fees/detail.html',
  ```

- `src/fees/views.py:64 Mutant #73`

  ```diff
  @@ -61,7 +61,7 @@
       fee = fee_application.fee_for(loan_id)
       return render(
           request,
  -        'fees/detail.html',
  +        'XXfees/detail.htmlXX',
           {
               'loan_id': loan_id,
               'fee': fee,
  ```

- `src/fees/views.py:66 Mutant #74`

  ```diff
  @@ -63,7 +63,7 @@
           request,
           'fees/detail.html',
           {
  -            'loan_id': loan_id,
  +            'XXloan_idXX': loan_id,
               'fee': fee,
               'amount': format_fee_amount(fee.amount_cents),
               'payment': context,
  ```

- `src/fees/views.py:67 Mutant #75`

  ```diff
  @@ -64,7 +64,7 @@
           'fees/detail.html',
           {
               'loan_id': loan_id,
  -            'fee': fee,
  +            'XXfeeXX': fee,
               'amount': format_fee_amount(fee.amount_cents),
               'payment': context,
           },
  ```

- `src/fees/views.py:68 Mutant #76`

  ```diff
  @@ -65,7 +65,7 @@
           {
               'loan_id': loan_id,
               'fee': fee,
  -            'amount': format_fee_amount(fee.amount_cents),
  +            'XXamountXX': format_fee_amount(fee.amount_cents),
               'payment': context,
           },
           status=status,
  ```

- `src/fees/views.py:69 Mutant #77`

  ```diff
  @@ -66,7 +66,7 @@
               'loan_id': loan_id,
               'fee': fee,
               'amount': format_fee_amount(fee.amount_cents),
  -            'payment': context,
  +            'XXpaymentXX': context,
           },
           status=status,
       )
  ```

- `src/fees/gateway.py:7 Mutant #78`

  ```diff
  @@ -4,7 +4,7 @@
   from .services import GatewayResponse, PaymentGatewayFailure
  -DEFAULT_PAYMENT_GATEWAY_URL = 'https://payments.lending-library.invalid'
  +DEFAULT_PAYMENT_GATEWAY_URL = 'XXhttps://payments.lending-library.invalidXX'
   class _NoRedirect(HTTPRedirectHandler):
  ```

- `src/fees/gateway.py:7 Mutant #79`

  ```diff
  @@ -4,7 +4,7 @@
   from .services import GatewayResponse, PaymentGatewayFailure
  -DEFAULT_PAYMENT_GATEWAY_URL = 'https://payments.lending-library.invalid'
  +DEFAULT_PAYMENT_GATEWAY_URL = None
   class _NoRedirect(HTTPRedirectHandler):
  ```

- `src/fees/gateway.py:26 Mutant #85`

  ```diff
  @@ -23,7 +23,7 @@
           try:
               with _open(request) as response:
  -                body = response.read().decode(response.headers.get_content_charset() or 'utf-8')
  +                body = response.read().decode(response.headers.get_content_charset() or 'XXutf-8XX')
                   return GatewayResponse(response.status, body)
           except HTTPError as response:
               with response:
  ```

- `src/fees/gateway.py:26 Mutant #86`

  ```diff
  @@ -23,7 +23,7 @@
           try:
               with _open(request) as response:
  -                body = response.read().decode(response.headers.get_content_charset() or 'utf-8')
  +                body = response.read().decode(response.headers.get_content_charset() and 'utf-8')
                   return GatewayResponse(response.status, body)
           except HTTPError as response:
               with response:
  ```

- `src/fees/gateway.py:30 Mutant #88`

  ```diff
  @@ -27,7 +27,7 @@
                   return GatewayResponse(response.status, body)
           except HTTPError as response:
               with response:
  -                body = response.read().decode(response.headers.get_content_charset() or 'utf-8')
  +                body = response.read().decode(response.headers.get_content_charset() or 'XXutf-8XX')
                   return GatewayResponse(response.code, body)
           except InterruptedError as error:
               raise PaymentGatewayFailure('payment gateway unavailable\n') from error
  ```

- `src/fees/gateway.py:30 Mutant #89`

  ```diff
  @@ -27,7 +27,7 @@
                   return GatewayResponse(response.status, body)
           except HTTPError as response:
               with response:
  -                body = response.read().decode(response.headers.get_content_charset() or 'utf-8')
  +                body = response.read().decode(response.headers.get_content_charset() and 'utf-8')
                   return GatewayResponse(response.code, body)
           except InterruptedError as error:
               raise PaymentGatewayFailure('payment gateway unavailable\n') from error
  ```

- `src/fees/gateway.py:33 Mutant #91`

  ```diff
  @@ -30,7 +30,7 @@
                   body = response.read().decode(response.headers.get_content_charset() or 'utf-8')
                   return GatewayResponse(response.code, body)
           except InterruptedError as error:
  -            raise PaymentGatewayFailure('payment gateway unavailable\n') from error
  +            raise PaymentGatewayFailure('XXpayment gateway unavailable\nXX') from error
           except OSError as error:
               raise PaymentGatewayFailure('payment gateway unavailable\n') from error
  ```

- `src/fees/gateway.py:35 Mutant #92`

  ```diff
  @@ -32,5 +32,5 @@
           except InterruptedError as error:
               raise PaymentGatewayFailure('payment gateway unavailable\n') from error
           except OSError as error:
  -            raise PaymentGatewayFailure('payment gateway unavailable\n') from error
  +            raise PaymentGatewayFailure('XXpayment gateway unavailable\nXX') from error
  ```

- `src/loans/forms.py:7 Mutant #93`

  ```diff
  @@ -4,7 +4,7 @@
   class LoanForm(forms.ModelForm):
  -    member = forms.CharField(strip=False)
  +    member = forms.CharField(strip=True)
       isbn = forms.CharField(strip=False)
       class Meta:
  ```

- `src/loans/forms.py:7 Mutant #94`

  ```diff
  @@ -4,7 +4,7 @@
   class LoanForm(forms.ModelForm):
  -    member = forms.CharField(strip=False)
  +    member = None
       isbn = forms.CharField(strip=False)
       class Meta:
  ```

- `src/loans/forms.py:8 Mutant #95`

  ```diff
  @@ -5,7 +5,7 @@
   class LoanForm(forms.ModelForm):
       member = forms.CharField(strip=False)
  -    isbn = forms.CharField(strip=False)
  +    isbn = forms.CharField(strip=True)
       class Meta:
           model = Loan
  ```

- `src/loans/forms.py:8 Mutant #96`

  ```diff
  @@ -5,7 +5,7 @@
   class LoanForm(forms.ModelForm):
       member = forms.CharField(strip=False)
  -    isbn = forms.CharField(strip=False)
  +    isbn = None
       class Meta:
           model = Loan
  ```

- `src/loans/forms.py:17 Mutant #104`

  ```diff
  @@ -14,7 +14,7 @@
       def clean_member(self):
           member = self.cleaned_data['member']
           if not member.strip():
  -            raise forms.ValidationError('This field is required.')
  +            raise forms.ValidationError('XXThis field is required.XX')
           return member
       def clean_isbn(self):
  ```

- `src/loans/forms.py:23 Mutant #108`

  ```diff
  @@ -20,6 +20,6 @@
       def clean_isbn(self):
           isbn = self.cleaned_data['isbn']
           if not isbn.strip():
  -            raise forms.ValidationError('This field is required.')
  +            raise forms.ValidationError('XXThis field is required.XX')
           return isbn
  ```

- `src/library_info/views.py:7 Mutant #109`

  ```diff
  @@ -3,8 +3,6 @@
   from django.template.loader import render_to_string
   from django.views.decorators.http import require_GET
  -
  -@require_GET
   def about(request):
       return HttpResponse(
           render_to_string('library_info/legacy_about.html'),
  ```

- `src/library_info/views.py:10 Mutant #110`

  ```diff
  @@ -7,7 +7,7 @@
   @require_GET
   def about(request):
       return HttpResponse(
  -        render_to_string('library_info/legacy_about.html'),
  +        render_to_string('XXlibrary_info/legacy_about.htmlXX'),
           content_type='text/html',
       )
  ```

- `src/library_info/views.py:11 Mutant #111`

  ```diff
  @@ -8,7 +8,7 @@
   def about(request):
       return HttpResponse(
           render_to_string('library_info/legacy_about.html'),
  -        content_type='text/html',
  +        content_type='XXtext/htmlXX',
       )
  ```

- `src/library_info/views.py:15 Mutant #112`

  ```diff
  @@ -11,8 +11,6 @@
           content_type='text/html',
       )
  -
  -@require_GET
   def about_page(request):
       return render(request, 'library_info/about.html')
  ```

- `src/library_info/views.py:17 Mutant #113`

  ```diff
  @@ -14,5 +14,5 @@
   @require_GET
   def about_page(request):
  -    return render(request, 'library_info/about.html')
  +    return render(request, 'XXlibrary_info/about.htmlXX')
  ```

