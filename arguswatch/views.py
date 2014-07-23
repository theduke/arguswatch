from django.shortcuts import render
from django.db.models import Q

from .argus_services.models import Service

def dashboard(request):
    services_critical = Service.objects.filter(
        state__in=(Service.STATE_DOWN, Service.STATE_UNKNOWN),
        state_provisional=False
    ).all()

    services_warning = Service.objects.filter(
        Q(state_provisional=True) | Q(state=Service.STATE_WARNING)
    ).all()

    return render(request, 'argus/dashboard.html', {
        'services_critical': services_critical,
        'services_warning': services_warning,
    })
