from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

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


@require_http_methods(['GET', 'POST'])
def loan_collection(request):
    if request.method == 'POST':
        return loan_lend(request)
    return HttpResponse(list_loans_text(), content_type='text/plain')


def loan_lend(request):
    form = LoanForm(request.POST)
    if not form.is_valid():
        errors = '\n'.join(
            f'{field}: {message}' for field, messages in form.errors.items() for message in messages
        )
        return HttpResponse(errors, status=400, content_type='text/plain')

    loan = lend_loan(**form.cleaned_data)
    return HttpResponse(loan_line(loan), status=201, content_type='text/plain')


@require_http_methods(['GET', 'POST'])
def loan_lend_page(request):
    form = LoanForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        loan = lend_loan(**form.cleaned_data)
        if request.headers.get('HX-Request') == 'true':
            return render(request, 'loans/loan-created.html', {'loan': loan})
        return redirect(f'/ui/loans/{loan.id}/')
    template = (
        'loans/loan-form.html'
        if request.method == 'POST' and request.headers.get('HX-Request') == 'true'
        else 'loans/new.html'
    )
    return render(request, template, {'form': form})


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


@require_POST
def loan_return_page(request, loan_id):
    loan, updated = return_loan(loan_id)
    if loan is None:
        return HttpResponse('no such loan\n', status=404, content_type='text/plain')

    if request.headers.get('HX-Request') == 'true':
        return render(
            request,
            'loans/return-status.html',
            {'loan': loan, 'updated': updated},
        )
    if not updated:
        return render(
            request,
            'loans/detail.html',
            {'loan': loan, 'return_error': True},
            status=409,
        )
    return redirect(f'/ui/loans/{loan.id}/')
