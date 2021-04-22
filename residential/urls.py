from django.urls import path
from residential.views import menu, auth, create, update


app_name = 'residential'

urlpatterns = [

    # sidebar menu urls
    path('', menu.DashboardPage, name='dashboard'),
    path('settings/', menu.SettingsPage, name='residential-settings'),
    path('main-counters/', menu.MainCountersPage, name='main_counters'),
    path('apartments/', menu.ApartmentsPage, name='apartments'),
    path('payments/', menu.PaymentsPage, name='payments'),

    # user/admin registration urls
    path('register/', auth.RegisterPage, name='register'),
    path('login/', auth.LoginPage, name='login'),
    path('logout/', auth.LogoutUser, name='logout'),

    # crud operations: create
    path('create-residential/', create.CreateResidential, name='create_residential'),
    path('create-utility/', create.CreateUtility, name='create_utility'),
    path('apartment-<int:pk>/create-tenant/', create.AssignTenant, name='assign-tenant'),

    # crud operations: update
    path('utility/apartment-<int:pk>/status-update/', update.UpdateUtilStatus, name='update_status'),
    path('utility/apartment-<int:pk>/update/', update.UpdateUtilityGeneral, name='update-utility'),

    path('counter/<int:pk>/update', update.UpdateMainCounters, name='update-main-counter'),

    path('apartment-<int:pk>/update-tenant/', update.UpdateTenant, name='update-tenant'),
]