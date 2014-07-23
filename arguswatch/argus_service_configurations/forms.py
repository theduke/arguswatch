from django import forms

from django_baseline.forms import CrispyModelForm

from .models import ServiceConfiguration


class ServiceConfigurationForm(CrispyModelForm):

    class Meta:
        model = ServiceConfiguration
        fields = [
            'name', 'description',
            
            'check_interval_ok',
            'check_interval_provisional',
            'check_interval_warning',
            'check_interval_down',
            'check_interval_unknown',

            'max_retries',

            'api_can_trigger_events',
        ]

    def __init__(self, *args, **kwargs):
        super(ServiceConfigurationForm, self).__init__(*args, **kwargs)
