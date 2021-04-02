from django.urls import path
from building import views

app_name = 'building'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('settings/', views.admin_settings, name='settings'),
    path('counters/', views.admin_counters, name='counters'),
    path('payments/', views.admin_payments, name='payments'),

    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('create-residential/', views.add_residential, name='create_residential'),
    path('add-new-util/', views.add_utility, name='add_new_util'),
]