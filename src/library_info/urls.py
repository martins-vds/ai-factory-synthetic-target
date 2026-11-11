from django.urls import path

from . import views

urlpatterns = [
    path('about', views.about),
    path('ui/about/', views.about_page),
]
