from django.shortcuts import render

from .argus_services.models import Service

def dashboard(request):
    services_critical = Service.objects.filter(
        state__in=(Service.STATE_WARNING, Service.STATE_CRITICAL),
        state_type=Service.STATE_TYPE_HARD).all()
    services_warning = Service.objects.filter(
        state__in=(Service.STATE_WARNING, Service.STATE_CRITICAL),
        state_type=Service.STATE_TYPE_SOFT
    ).all()

    return render(request, 'argus/dashboard.html', {
        'services_critical': services_critical,
        'services_warning': services_warning,
    })
