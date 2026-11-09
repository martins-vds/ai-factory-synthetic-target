from django.urls import path

from . import views

urlpatterns = [
    path('loans', views.loan_list, name='loan-list'),
    path('loans/<str:loan_id>', views.loan_detail, name='loan-detail'),
]
