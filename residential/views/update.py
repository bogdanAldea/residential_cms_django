from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from residential.views.menu import get_logged
from residential.forms import UpdateUtilityForm, CreateTenant
from apartment.models import Apartment, IndividualUtil


def UpdateUtilStatus(request, pk):
    """
    Defined view that handles the update of selected apartment's utility status
    through a formset.
    """

    # retrieve currently logged user and the building he's managing
    # logged_admin = User.objects.get(username=request.user.username)
    # building = Building.objects.get(admin=logged_admin)

    _, building = get_logged(request)

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


def UpdateUtilityGeneral(request, pk):
    """
    Defined view that handles the update of utilities that belong only to the
    current working building.
    """

    # retrieve currently logged user and the building he's managing
    # logged_admin = User.objects.get(username=request.user.username)
    # building = Building.objects.get(admin=logged_admin)
    _, building = get_logged(request)

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


def UpdateTenant(request, pk):
    """
    Defined view that allows tenant selection through the template
    and allows information updates.
    """

    # retrieve building manager by the currently log administrator
    _, building = get_logged(request)

    # instantiate tenant form
    apartment = building.apartment_set.get(id=pk)
    form = CreateTenant(instance=apartment.tenant)
    if request.method == 'POST':
        form = CreateTenant(request.POST, instance=apartment.tenant)
        if form.is_valid():
            user = form.save()
            return redirect('residential:tenants')

    context = {'form': form}
    return render(request, 'residential/forms/update_tenant.html', context)