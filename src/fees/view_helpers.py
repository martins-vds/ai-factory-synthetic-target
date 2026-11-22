from django.http import HttpResponse

from .composition import fee_application
from .services import PaymentGatewayFailure


def format_fee_amount(amount_cents):
    return f'${amount_cents // 100}.{amount_cents % 100:02d}'


def gateway_result(loan_id):
    try:
        result = fee_application.pay(loan_id)
    except PaymentGatewayFailure as error:
        return error.body, 502
    if result is None:
        return None, 404
    return result.body, 200 if result.status == 200 else 502


def fee_or_404(loan_id):
    fee = fee_application.fee_for(loan_id)
    if fee is None:
        return HttpResponse('<p>No such loan.</p>', status=404, content_type='text/html')
    return fee
