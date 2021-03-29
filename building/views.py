from django.shortcuts import render
from .models import *


def admin_dashboard(request):
    building = Building.objects.first()
    apartments = Apartment.objects.all().filter(building=building)
    context = {
        'building': building,
        'occupied': len(apartments.filter(number_of_persons__gt=0)),
        'apartments_all': apartments,
    }

    return render(request, 'building/dashboard.html', context)


def admin_settings(request):
    user = User.objects.get(username='bogdan')
    building = Building.objects.get(admin=user)

    # Queryset for mutual utilities
    mutual_utils = MutualUtil.objects.all().\
        filter(common_util__building=building)

    supply_data = IndividualUtil.objects.all().\
        filter(individual_util__building=building).\
        order_by('individual_util__name')

    # Queryset for displaying all apartments and their settings
    apartments = Apartment.objects.all().\
        filter(building=building)

    context = {
        'mutual_utils': mutual_utils,
        'supply_data': supply_data.order_by('individual_util__name'),
        'apartments': apartments
    }

    return render(request, 'building/settings.html', context)


def admin_counters(request):
    return render(request, 'building/counters.html')


def admin_payments(request):
    return render(request, 'building/payments.html')

