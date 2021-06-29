from django.urls import path
from .views import menu, auth

app_name = 'building'

urlpatterns = [

    # sidebar urls
    path("", menu.DashboardPage, name="admin_dashboard"),
    path("settings/", menu.SettingsPage, name="admin_settings"),
    path("apartments/", menu.ApartmentsPage, name="admin_apartments"),
    path("payments/", menu.PaymentsPage, name="admin_payments"),
    path("documents/", menu.DocumentsPage, name="admin_documents"),

    # user authentication urls
    path('register/', auth.RegisterPage, name='register'),
    path('login/', auth.LoginPage, name='login'),
    path('logout/', auth.LogoutUser, name='logout'),
]