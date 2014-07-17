from django import forms

from django_baseline.forms import CrispyModelForm

from ..argus_service_configurations.models import ServiceConfiguration

from .models import Service
from .plugins import ServicePlugin


class ServiceForm(CrispyModelForm):

    class Meta:
        model = Service
        fields = ['name', 'description', 'service_config',  'parent', 'tags', 'plugin']


    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['plugin'] = forms.ChoiceField(choices=ServicePlugin.get_plugin_choices())

        qs = ServiceConfiguration.objects.filter(is_template=True)
        self.fields['service_config'] = forms.ModelChoiceField(queryset=qs, empty_label=None)
