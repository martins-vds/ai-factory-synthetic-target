from html import escape

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .composition import fee_application
from .services import PaymentGatewayFailure


def _fee_amount(amount_cents):
    return f'${amount_cents // 100}.{amount_cents % 100:02d}'


def _gateway_result(loan_id):
    try:
        result = fee_application.pay(loan_id)
    except PaymentGatewayFailure as error:
        return error.body, 502
    if result is None:
        return None, 404
    return result.body, 200 if result.status == 200 else 502


@require_GET
def fee_detail(request, loan_id):
    fee = fee_application.fee_for(loan_id)
    if fee is None:
        return HttpResponse('<p>No such loan.</p>', status=404, content_type='text/html')

    body = (
        f'<h1>Late fee for {escape(loan_id)}</h1>'
        f'<p>Due {fee.due_on.isoformat()}, {fee.days_late} day(s) late.</p>'
        f'<p class="fee">Fee: {_fee_amount(fee.amount_cents)}</p>'
    )
    return HttpResponse(body, content_type='text/html')


@require_POST
def payment(request, loan_id):
    body, status = _gateway_result(loan_id)
    if status == 404:
        return HttpResponse('no such loan\n', status=404, content_type='text/plain')
    return HttpResponse(body, status=status, content_type='text/plain')


@require_GET
def fee_page(request, loan_id):
    fee = fee_application.fee_for(loan_id)
    if fee is None:
        return HttpResponse('<p>No such loan.</p>', status=404, content_type='text/html')
    return render(
        request,
        'fees/detail.html',
        {'loan_id': loan_id, 'fee': fee, 'amount': _fee_amount(fee.amount_cents)},
    )


@require_POST
def payment_page(request, loan_id):
    body, status = _gateway_result(loan_id)
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
            'amount': _fee_amount(fee.amount_cents),
            'payment': context,
        },
        status=status,
    )
