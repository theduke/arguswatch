from django import forms

from django_baseline.forms import CrispyModelForm

from .models import Service
from .plugins import ServicePlugin


class ServiceForm(CrispyModelForm):

    class Meta:
        model = Service
        fields = ['name', 'description', 'parent', 'tags', 'plugin']


    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['plugin'] = forms.ChoiceField(choices=ServicePlugin.get_plugin_choices())
