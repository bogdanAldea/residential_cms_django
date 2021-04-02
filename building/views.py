from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from .config import UtilType


# View for building's admin dashboard
def admin_dashboard(request):
    user = User.objects.get(username=request.user.username)
    try:
        building = Building.objects.get(admin=user)
    except Building.DoesNotExist:
        return redirect('building:create_residential')

    apartments = Apartment.objects.filter(building=building)
    occupied = apartments.filter(number_of_persons__gt=0)

    context = {
        'building': building,
        'apartments': apartments,
        'occupied': occupied,
    }

    return render(request, 'building/dashboard.html', context)


# View for building's admin settings
def admin_settings(request):
    user = User.objects.get(username=request.user.username)
    building = Building.objects.get(admin=user)

    # Queryset for mutual utilities
    mutual_utils = Utility.objects.filter(
        util_type=UtilType.mutual,
        building=building
    )

    supply_data = Utility.objects.filter(
        util_type=UtilType.individual,
        building=building
    )

    features_data = FeatureLinked.objects.all().\
        filter(related_feature__building=building)

    # Queryset for displaying all apartments and their settings
    apartments = Apartment.objects.all().\
        filter(building=building)

    context = {
        'mutual_utils': mutual_utils,
        'supply_data': supply_data.order_by('name'),
        'features_data': features_data,
        'apartments': apartments,
    }

    return render(request, 'building/settings.html', context)


# View for building's admin counters
def admin_counters(request):
    return render(request, 'building/counters.html')


# View for building's admin apartment payments
def admin_payments(request):
    return render(request, 'building/payments.html')


# View for building admin creation/registration
def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('building:login')

    context = {'form': form}
    return render(request, 'building/register.html', context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('building:dashboard')

    return render(request, 'building/login.html')


def logout_user(request):
    logout(request)
    return redirect('building:login')


# View for building creation when building queryset is 0.
# Redirected here form admin login is requested admin has no building under administration
def add_residential(request):
    form = CreateResidentialForm()

    if request.method == 'POST':
        form = CreateResidentialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('building:dashboard')
    context = {'form': form}
    return render(request, 'building/create_residential.html', context)


# View for creating a new utility objects
def add_utility(request):
    logged_admin = User.objects.get(username=request.user.username)
    cw_building = Building.objects.get(admin=logged_admin)

    form = CreateUtilForm()
    if request.method == 'POST':
        form = CreateUtilForm(request.POST)
        if form.is_valid():
            util = form.save(commit=False)
            util.building = cw_building
            util.save()
            return redirect('building:settings')

    context = {'form': form}
    return render(request, 'building/add_utility.html', context)