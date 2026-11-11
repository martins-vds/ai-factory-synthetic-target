import os
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .services import GatewayResponse, PaymentGatewayFailure

DEFAULT_PAYMENT_GATEWAY_URL = 'https://payments.lending-library.invalid'


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, new_url):
        return None


def _open(request):
    return build_opener(_NoRedirect()).open(request)


class HttpPaymentGateway:
    def charge(self, loan_id):
        gateway_url = os.environ.get('PAYMENT_GATEWAY_URL', DEFAULT_PAYMENT_GATEWAY_URL)
        request = Request(f'{gateway_url}/charge?loan={loan_id}', method='POST')

        try:
            with _open(request) as response:
                body = response.read().decode(response.headers.get_content_charset() or 'utf-8')
                return GatewayResponse(response.status, body)
        except HTTPError as response:
            with response:
                body = response.read().decode(response.headers.get_content_charset() or 'utf-8')
                return GatewayResponse(response.code, body)
        except InterruptedError as error:
            raise PaymentGatewayFailure('payment gateway unavailable\n') from error
        except OSError as error:
            raise PaymentGatewayFailure('payment gateway unavailable\n') from error
