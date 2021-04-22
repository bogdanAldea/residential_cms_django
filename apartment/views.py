from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from residential.views.menu import get_logged
from .models import Apartment, IndividualUtil


def UpdateApartmentCounters(request, pk):
    """

    """
    # retrieve building managed by the currently logged user
    _, building = get_logged(request)

    # define formset
    CounterFormset = inlineformset_factory(
        parent_model=Apartment, model=IndividualUtil,
        fields=('index_counter',), extra=0
    )

    # select apartment by accessing its primary key
    apartment = building.apartment_set.get(id=pk)
    counters  = apartment.individualutil_set.all()

    # define formset by passing the queried apartment object
    formset = CounterFormset(instance=apartment)
    if request.method == 'POST':
        formset = CounterFormset(request.POST, instance=apartment)
        if formset.is_valid():
            formset.save()
            return redirect('residential:apartments')

    form_data = zip(counters, formset)

    context = {
        'formset': formset,
        'form_data': form_data
    }
    return render(request, 'residential/forms/update_apartment_counters.html', context)