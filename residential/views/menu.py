from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from residential.models import User, Building

def get_logged(request):
    logged_admin = User.objects.get(username=request.user.username)
    building = Building.objects.get(admin=logged_admin)
    return logged_admin, building


@login_required(login_url='residential:login')
def DashboardPage(request):
    """
    Defined view function that handles the rendering of the data required by the
    dashboard.
    """

    # retrieve currently logged user with admin privileges
    user, _ = get_logged(request)

    # check if this user has already a building under administration
    try:
        # retrieve the building objects assigned to currently logged user
        building = Building.objects.get(admin=user)
    except Building.DoesNotExist:
        # if there is no building assigned to this user, redirect user to a building creation form
        return redirect('residential:create_residential')

    # define context data to render inside the template
    apartments_list             = building.apartment_set.all()
    occupied_apartments_list    = apartments_list.filter(persons__gt=0)

    context = {
        'building': building,
        'apartments_list': apartments_list,
        'occupied_apartments_list': occupied_apartments_list
    }

    return render(request, 'residential/menu/dashboard.html', context)


@login_required(login_url='residential:login')
def SettingsPage(request):
    """
    Defined view that renders data for the building settings page.
    """

    # retrieve building that has as admin the currently logged user
    _, building = get_logged(request)

    # retrieve queryset for individual utilities & power supplies
    power_supplies = building.utility_set.filter(util_type='Individual')

    # retrieve queryset for mutual utilities & facilities
    mutual_utils = building.utility_set.filter(util_type='Mutual')

    # retrieve apartment queryset that belongs to currently logged admin's building
    apartments = building.apartment_set.all()

    context = {
        'power_supplies': power_supplies,
        'mutual_utils': mutual_utils,
    }
    return render(request, 'residential/menu/residential_settings.html', context)


@login_required(login_url='residential:login')
def ApartmentsPage(request):
    """
    Defined view that renders all apartments and allows handling of tenant assignment through the template.
    """

    # retrieve building managed by the currently logged administrator.
    _, building = get_logged(request)

    context = {'building': building}
    return render(request, 'residential/menu/apartments.html', context)


@login_required(login_url='residential:login')
def PaymentsPage(request):
    """
    Defined view that renders all apartments and the expenses
    and allows admin user to process each apartments payments.
    """

    # retrieve building managed by the currently logged administrator.
    _, building = get_logged(request)



    context = {'building': building}
    return render(request, 'residential/menu/payments.html', context)