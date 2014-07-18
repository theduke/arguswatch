from django import forms

from django_baseline.forms import CrispyModelForm

from .models import Notification
from .plugins import NotificationPlugin


class NotificationForm(CrispyModelForm):

    class Meta:
        model = Notification
        fields = ['name', 'description', 'plugin',
            'on_remains_up', 
            'on_critical_soft', 'on_warning_soft', 'on_recovery_soft',
            'on_critical_hard', 'on_warning_hard', 'on_recovery_hard',

            'interval', 'interval_remains_up', 'interval_warning_hard',
            'interval_critical_hard', 'interval_recovery_hard',
        ]


    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.fields['plugin'] = forms.ChoiceField(choices=NotificationPlugin.get_plugin_choices())
