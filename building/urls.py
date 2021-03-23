from django.urls import path
from building import views

app_name = 'building'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('settings/', views.admin_settings, name='settings'),
    path('counters/', views.admin_counters, name='counters'),
    path('payments/', views.admin_payments, name='payments'),
]