from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *

"""DEFINED VIEWS FOR SIDEBAR/MAIN MENU LINKS"""
def DashboardPage(request):
    """
    Defined view function that handles the rendering of the data required by the
    dashboard.
    """

    # retrieve currently logged user with admin prvileges
    user = User.objects.get(username=request.user.username)

    # check if this user has already a building under administration
    try:
        # retrieve the building objects assigned to currently logged user
        building = Building.objects.get(admin=user)
    except Building.DoesNotExist:
        # if there is no building assigned to this user, redirect user to a building creation form
        return redirect('building:create_residential')

    # define context data to render inside the template
    apartments  = building.apartment_set.all()
    occupied    = apartments.filter(persons__gt=0)

    context = {
        'building': building,
        'apartments': apartments,
        'occupied': occupied
    }

    return render(request, 'residential/menu/dashboard.html', context)


def SettingsPage(request):
    """
    Defined view that renders data for the building settings page.
    """

    # retrieve building that has as admin the currently logged user
    user = User.objects.get(username=request.user.username)
    building = Building.objects.get(admin=user)

    # retrieve queryset for individual utilities & power supplies
    power_supplies = building.utility_set.filter(util_type='Individual')

    # retrieve queryset for mutual utilities & facilities
    mutual_utils = building.utility_set.filter(util_type='Mutual')

    # retrieve apartment queryset that belongs to currently logged admin's building
    apartments = building.apartment_set.all()

    context = {
        'power_supplies': power_supplies,
        'mutual_utils': mutual_utils,
        'apartments': apartments
    }
    return render(request, 'residential/menu/residential_settings.html', context)


"""DEFINE VIEWS FOR ADMIN USER AUTHENTICATION"""
def RegisterPage(request):
    """
    Defined view that handles new user registration with admin privileges.
    """

    # instantiate new form for user registration
    form = UserCreationForm()

    # check type of method request
    if request.method == 'POST':
        # pass the request method to the form
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect user to login page after registration form is submitted
            return redirect('building:login')

    # context data to render in the template
    context = {'form': form}
    return render(request, 'residential/registration/register.html', context)


def LoginPage(request):
    """
    Defined view that handles the user login (user with admin privileges).
    """

    # check type of request method
    if request.method == 'POST':
        # retrieve user's login credentials
        username = request.POST.get('username')
        password = request.POST.get('password')

        # attempt user authentication
        user = authenticate(request, username=username, password=password)

        # authenticate user if exists
        if user is not None:
            login(request, user)
            # redirect admin-user to admin panel
            return redirect('building:dashboard')
    return render(request, 'residential/registration/login.html')


def LogoutUser(request):
    """
    Defined view that handles user's logout.
    """
    logout(request)
    return  redirect('building:login')


"""DEFINE VIEWS THAT HANDLE RESIDENTIAL BUSINESS LOGIC"""
def CreateResidential(request):
    """
    Defined View that handles residential building creation.
    When a new user with admin privileges is registered, he's redirected to a form that handles
    creation of a new custom building object.
    """
    form = CreateResidentialForm()
    if request.method == 'POST':
        form = CreateResidentialForm(request.POST)
        if form.is_valid():
            residential = form.save(commit=False)
            residential.admin = request.user
            residential.save()
            return redirect('building:dashboard')

    context = {'form': form}
    return render(request, 'residential/forms/create_residential.html', context)


def CreateUtility(request):
    """
    Defined view that handles creation of a new general utility. After a new utility instance is created,
    the model sends a signal which triggers the function that generates an utility instance for each existing apartment.
    """

    logged_admin = User.objects.get(username=request.user.username)
    building = Building.objects.get(admin=logged_admin)

    # instantiate utility creation form
    form = CreateUtilityForm()

    # check type of request method
    if request.method == 'POST':
        # pass request method to creation form
        form = CreateUtilityForm(request.POST)
        if form.is_valid():
            util = form.save(commit=False)
            # auto-assign the newly created util to current working building
            util.building = building
            util.save()
            return redirect('residential:residential-settings')

    context = {'form': form}
    return render(request, 'residential/forms/create_utility.html', context)