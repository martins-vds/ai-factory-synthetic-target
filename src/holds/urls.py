from django.urls import path

from . import views

urlpatterns = [
    path('holds', views.hold_collection),
    path('holds/<str:hold_id>/cancel', views.hold_cancel),
]
