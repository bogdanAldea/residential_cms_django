from django.shortcuts import render


def admin_dashboard(request):
    return render(request, 'building/dashboard.html')


def admin_settings(request):
    return render(request, 'building/settings.html')


def admin_counters(request):
    return render(request, 'building/counters.html')


def admin_payments(request):
    return render(request, 'building/payments.html')

