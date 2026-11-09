from django.urls import path

from . import views

urlpatterns = [
    path('loans', views.loan_list, name='loan-list'),
    path('loans/<str:loan_id>', views.loan_detail, name='loan-detail'),
    path('ui/loans/', views.loan_catalog, name='loan-catalog'),
    path('ui/loans/<str:loan_id>/', views.loan_catalog_detail, name='loan-catalog-detail'),
]
