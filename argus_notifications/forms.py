from django import forms

from django_baseline.forms import CrispyModelForm

from .models import Notification
from .plugins import NotificationPlugin


class NotificationForm(CrispyModelForm):

    class Meta:
        model = Notification
        fields = ['name', 'description', 'plugin',
            'on_ok', 
            'on_soft_critical', 'on_soft_warning', 'on_soft_recovery',
            'on_hard_critical', 'on_hard_warning', 'on_hard_recovery',
            'always_on_hard_recovery',

            'interval', 'interval_ok', 'interval_hard_warning',
        ]


    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.fields['plugin'] = forms.ChoiceField(choices=NotificationPlugin.get_plugin_choices())
