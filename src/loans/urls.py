from django.urls import path

from . import views

urlpatterns = [
    path('loans', views.loan_collection),
    path('loans/<str:loan_id>/return', views.loan_return),
    path('loans/<str:loan_id>', views.loan_detail),
    path('ui/loans/', views.loan_catalog),
    path('ui/loans/new/', views.loan_lend_page),
    path('ui/loans/<str:loan_id>/return/', views.loan_return_page),
    path('ui/loans/<str:loan_id>/', views.loan_catalog_detail),
]
