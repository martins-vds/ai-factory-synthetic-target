from html import escape

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .composition import fee_application
from .view_helpers import fee_or_404, format_fee_amount, gateway_result


@require_GET
def fee_detail(request, loan_id):
    fee = fee_or_404(loan_id)
    if isinstance(fee, HttpResponse):
        return fee

    body = (
        f'<h1>Late fee for {escape(loan_id)}</h1>'
        f'<p>Due {fee.due_on.isoformat()}, {fee.days_late} day(s) late.</p>'
        f'<p class="fee">Fee: {format_fee_amount(fee.amount_cents)}</p>'
    )
    return HttpResponse(body, content_type='text/html')


@require_POST
def payment(request, loan_id):
    body, status = gateway_result(loan_id)
    if status == 404:
        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
    return HttpResponse(body, status=status, content_type='text/plain')


@require_GET
def fee_page(request, loan_id):
    fee = fee_or_404(loan_id)
    if isinstance(fee, HttpResponse):
        return fee

    return render(
        request,
        'fees/detail.html',
        {'loan_id': loan_id, 'fee': fee, 'amount': format_fee_amount(fee.amount_cents)},
    )


@require_POST
def payment_page(request, loan_id):
    body, status = gateway_result(loan_id)
    if status == 404:
        return HttpResponse('no such loan\n', status=404, content_type='text/plain')

    context = {'body': body, 'success': status == 200}
    if request.headers.get('HX-Request') == 'true':
        return render(
            request,
            'fees/payment-status.html',
            context,
            status=status,
        )

    fee = fee_application.fee_for(loan_id)
    return render(
        request,
        'fees/detail.html',
        {
            'loan_id': loan_id,
            'fee': fee,
            'amount': format_fee_amount(fee.amount_cents),
            'payment': context,
        },
        status=status,
    )
