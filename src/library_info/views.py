from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET


@require_GET
def about(request):
    return HttpResponse(
        render_to_string('library_info/legacy_about.html'),
        content_type='text/html',
    )


@require_GET
def about_page(request):
    return render(request, 'library_info/about.html')
