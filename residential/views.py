from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from apartment.models import Apartment, IndividualUtil
from .forms import *
from .decorators import *

"""DEFINED VIEWS FOR SIDEBAR/MAIN MENU LINKS"""
@login_required(login_url='residential:login')
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

@login_required(login_url='residential:login')
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
@login_required(login_url='residential:login')
@unauthenticated_user
def RegisterPage(request):
    """
    Defined view that handles new user registration with admin privileges.
    """

    group = Group.objects.get(name='administrator')

    # instantiate new form for user registration
    form = CreateUSerForm()

    # check type of method request
    if request.method == 'POST':
        # pass the request method to the form
        form = CreateUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(group)
            user.save()
            # redirect user to login page after registration form is submitted
            return redirect('building:login')

    # context data to render in the template
    context = {'form': form}
    return render(request, 'residential/registration/register.html', context)


@unauthenticated_user
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
    return redirect('building:login')


"""DEFINE VIEWS THAT HANDLE RESIDENTIAL C.R.U.D. BUSINESS LOGIC"""
@login_required(login_url='residential:login')
def CreateResidential(request):
    """
    Defined View that handles residential building creation.
    When a new user with admin privileges is registered, he's redirected to a form that handles
    creation of a new custom building object.
    """
    form = ResidentialForm()
    if request.method == 'POST':
        form = ResidentialForm(request.POST)
        if form.is_valid():
            residential = form.save(commit=False)
            residential.admin = request.user
            residential.save()
            return redirect('building:dashboard')

    context = {'form': form}
    return render(request, 'residential/forms/create_residential.html', context)


@login_required(login_url='residential:login')
def CreateUtility(request):
    """
    Defined view that handles creation of a new general utility. After a new utility instance is created,
    the model sends a signal which triggers the function that generates an utility instance for each existing apartment.
    """

    logged_admin = User.objects.get(username=request.user.username)
    building = Building.objects.get(admin=logged_admin)

    # instantiate utility creation form
    form = UtilityForm()

    # check type of request method
    if request.method == 'POST':
        # pass request method to creation form
        form = UtilityForm(request.POST)
        if form.is_valid():
            util = form.save(commit=False)
            # auto-assign the newly created util to current working building
            util.building = building
            util.save()
            return redirect('residential:residential-settings')

    context = {'form': form}
    return render(request, 'residential/forms/create_utility.html', context)


@login_required(login_url='residential:login')
def UpdateUtilStatus(request, pk):
    """
    Defined view that handles the update of selected apartment's utility status
    through a formset.
    """

    # retrieve currently logged user and the building he's managing
    logged_admin = User.objects.get(username=request.user.username)
    building = Building.objects.get(admin=logged_admin)

    # defined the formset that takes the apartment model as the parent argument
    # and the individual utility model as the child argument
    UtilFormset = inlineformset_factory(
        parent_model=Apartment, model=IndividualUtil,
        fields=('status',), extra=0
    )

    # select apartment by accessing its primary key
    apartment = building.apartment_set.get(id=pk)

    # define formset by passing the queried apartment object
    formset = UtilFormset(instance=apartment)
    if request.method == 'POST':
        # pass the request method to the defined formset
        formset = UtilFormset(request.POST, instance=apartment)
        if formset.is_valid():
            formset.save()
            # redirect suer back to the settings page
            return redirect('residential:residential-settings')

    # define context data to render into the template
    form_util_names = ['Cold Water', 'Hot Water', 'Gas Power', 'Heating Power']
    form_data = zip(form_util_names, formset)

    context = {
        'apartment': apartment,
        'form_data': form_data,
        'formset': formset,
    }
    return render(request, 'residential/forms/update_status.html', context)


@login_required(login_url='residential:login')
def UpdateUtilityGeneral(request, pk):
    """
    Defined view that handles the update of utilities that belong only to the
    current working building.
    """

    # retrieve currently logged user and the building he's managing
    logged_admin = User.objects.get(username=request.user.username)
    building = Building.objects.get(admin=logged_admin)

    # retrieve utilities used by current working building
    utility = building.utility_set.get(id=pk)

    form = UpdateUtilityForm(instance=utility)
    if request.method == 'POST':
        form = UpdateUtilityForm(request.POST, instance=utility)
        if form.is_valid():
            form.save()
            return redirect('residential:residential-settings')

    context = {'form': form}
    return render(request, 'residential/forms/update_utility.html', context)

