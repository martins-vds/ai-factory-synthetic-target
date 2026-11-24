from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_POST

from .composition import hold_application
from .services import HoldError, hold_line


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
    if isinstance(result, HoldError):
        return HttpResponse(
            f'{result.message}\n',
            status=result.status,
            content_type='text/plain',
        )
    return HttpResponse(hold_line(result), status=201, content_type='text/plain')


@require_POST
def hold_cancel(request, hold_id):
    result = hold_application.cancel(hold_id)
    if isinstance(result, HoldError):
        return HttpResponse(
            f'{result.message}\n',
            status=result.status,
            content_type='text/plain',
        )
    return HttpResponse(hold_line(result), content_type='text/plain')
