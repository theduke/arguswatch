from django import forms

from django_baseline.forms import CrispyModelForm

from .models import ServiceConfiguration


class ServiceConfigurationForm(CrispyModelForm):

    class Meta:
        model = ServiceConfiguration
        fields = [
            'name', 'description',
            'check_interval', 
            'retry_interval_soft', 'retry_interval_hard',
            'max_retries_soft',
        ]


    def __init__(self, *args, **kwargs):
        super(ServiceConfigurationForm, self).__init__(*args, **kwargs)
