from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_POST

from .composition import hold_application
from .services import HoldFailure, HoldFailureCode, hold_line

FAILURE_RESPONSES = {
    HoldFailureCode.REQUIRED_FIELDS: (400, 'member and isbn are required'),
    HoldFailureCode.BOOK_AVAILABLE: (409, 'book is available'),
    HoldFailureCode.BORROWER: (409, 'member has this book'),
    HoldFailureCode.DUPLICATE: (409, 'already on hold'),
    HoldFailureCode.HOLD_LIMIT: (409, 'hold limit reached'),
    HoldFailureCode.NOT_FOUND: (404, 'no such hold'),
    HoldFailureCode.ALREADY_CANCELLED: (409, 'hold already cancelled'),
}


def _failure_response(failure):
    status, message = FAILURE_RESPONSES[failure.code]
    return HttpResponse(f'{message}\n', status=status, content_type='text/plain')


@require_http_methods(['GET', 'POST'])
def hold_collection(request):
    if request.method == 'GET':
        return HttpResponse(
            hold_application.list_active_text(request.GET.get('isbn')),
            content_type='text/plain',
        )

    result = hold_application.place(
        request.POST.get('member', ''),
        request.POST.get('isbn', ''),
    )
    if isinstance(result, HoldFailure):
        return _failure_response(result)
    return HttpResponse(hold_line(result), status=201, content_type='text/plain')


@require_POST
def hold_cancel(request, hold_id):
    result = hold_application.cancel(hold_id)
    if isinstance(result, HoldFailure):
        return _failure_response(result)
    return HttpResponse(hold_line(result), content_type='text/plain')
