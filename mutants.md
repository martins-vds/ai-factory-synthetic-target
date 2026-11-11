# Surviving mutants: LI-ACCEPT

Written by `afs-mutation` on its last run (base `all`): score 0.976, threshold 0.8, killed 244, survived 6. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

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

- `src/loans/urls.py:9 Mutant #27`

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

- `src/fees/services.py:24 Mutant #1`

  ```diff
  @@ -21,7 +21,7 @@
       def charge(self, loan_id: str) -> 'GatewayResponse': ...
  -@dataclass(frozen=True)
  +@dataclass(frozen=False)
   class Fee:
       due_on: date
       days_late: int
  ```

- `src/fees/services.py:31 Mutant #3`

  ```diff
  @@ -28,7 +28,7 @@
       amount_cents: int
  -@dataclass(frozen=True)
  +@dataclass(frozen=False)
   class GatewayResponse:
       status: int
       body: str
  ```

- `src/loans/forms.py:8 Mutant #44`

  ```diff
  @@ -5,6 +5,6 @@
   class LoanForm(forms.ModelForm):
       class Meta:
  -        model = Loan
  +        model = None
           fields = ('member', 'isbn')
  ```

