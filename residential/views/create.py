from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from residential.forms import *
from residential.views.menu import get_logged
from apartment.models import Tenant, Apartment


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


def CreateUtility(request):
    """
    Defined view that handles creation of a new general utility. After a new utility instance is created,
    the model sends a signal which triggers the function that generates an utility instance for each existing apartment.
    """

    # logged_admin = User.objects.get(username=request.user.username)
    # building = Building.objects.get(admin=logged_admin)
    _, building = get_logged(request)

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


def AssignTenant(request, pk):
    """
    Defined view that handles the tenant profile creation and apartment assignment.
    View uses already created custom CreateUserFrom to create a new user placed in the
    tenant group.
    """

    _, building = get_logged(request)

    form = CreateTenant()
    if request.method == 'POST':
        form = CreateTenant(request.POST)
        if form.is_valid():
            user_as_tenant = form.save()

            # auto assign to group 'tenant'
            group = Group.objects.get(name='tenant')
            user_as_tenant.groups.add(group)

            # create new tenant objects/profile
            tenant = Tenant.objects.create(
                tenant=user_as_tenant,
                first_name=user_as_tenant.first_name,
                last_name=user_as_tenant.last_name,
                email=user_as_tenant.email,
                phone=user_as_tenant.phone
            )

            # filter apartment objects,
            # return the one belonging to current working building,
            # assign newly created tenant
            Apartment.objects.filter(id=pk, building=building).update(tenant=tenant)
            user_as_tenant.save()
            return redirect('residential:tenants')

    context = {'form': form}
    return render(request, 'residential/forms/assign_tenant.html', context)