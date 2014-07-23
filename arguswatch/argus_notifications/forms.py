from django import forms

from django_baseline.forms import CrispyModelForm

from .models import Notification
from .plugins import NotificationPlugin


class NotificationForm(CrispyModelForm):

    class Meta:
        model = Notification
        fields = ['name', 'description', 'plugin',
            'interval_state_change_provisional',
            'interval_state_stays_provisional',
            'interval_state_change', 
            'interval_state_stays',
            'interval_change_ok',
            'interval_hard',
        ]

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.fields['plugin'] = forms.ChoiceField(choices=NotificationPlugin.get_plugin_choices())
