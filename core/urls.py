# core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('analytics/', views.analytics_view, name='analytics'),
]

