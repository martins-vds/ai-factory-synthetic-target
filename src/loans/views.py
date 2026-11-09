from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render

from .forms import LoanForm
from .models import Loan
from .services import (
    get_loan_text,
    lend_loan,
    list_loans_text,
    loan_line,
    return_loan,
)


def loan_catalog(request):
    return render(request, 'loans/list.html', {'loans': Loan.objects.all()})


def loan_catalog_detail(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    return render(request, 'loans/detail.html', {'loan': loan})


def loan_collection(request):
    if request.method == 'POST':
        return loan_lend(request)
    return HttpResponse(list_loans_text(), content_type='text/plain')


def loan_lend(request):
    form = LoanForm(request.POST)
    if not form.is_valid():
        errors = '\n'.join(
            f'{field}: {message}'
            for field, messages in form.errors.items()
            for message in messages
        )
        return HttpResponse(errors, status=400, content_type='text/plain')

    loan = lend_loan(**form.cleaned_data)
    return HttpResponse(loan_line(loan), status=201, content_type='text/plain')


def loan_detail(request, loan_id):
    body = get_loan_text(loan_id)
    if body is None:
        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
    return HttpResponse(body, content_type='text/plain')


@require_POST
def loan_return(request, loan_id):
    loan, updated = return_loan(loan_id)
    if loan is None:
        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
    if not updated:
        return HttpResponse('already returned\n', status=409, content_type='text/plain')
    return HttpResponse(loan_line(loan), content_type='text/plain')
