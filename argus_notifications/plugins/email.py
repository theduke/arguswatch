from django.db import models
from django.utils.translation import ugettext as _

from django_baseline.forms import CrispyModelForm

from . import NotificationPlugin
from ..models import NotificationPluginConfiguration


class EmailPluginConfig(NotificationPluginConfiguration):
    emails = models.TextField(verbose_name='Multiple Email addresses you want to send to. Separated by semicolon (;).')
    subject = models.CharField(max_length=255, verbose_name='Email subject (Will be appended with service name and state)', blank=True)
    message = models.TextField('Email message body. Will be appended with service, state and description', blank=True)


    class Meta:
        verbose_name = _('EmailPluginConfig')
        verbose_name_plural = _('EmailPluginConfigs')
        app_label = "argus_notifications"


class EmailPluginForm(CrispyModelForm):
    class Meta:
        model = EmailPluginConfig
        fields = ['emails', 'subject', 'message']


class EmailNotification(NotificationPlugin):
    name = "Email"
    description = "Send Email."
    config_class = EmailPluginConfig
    form_class = EmailPluginForm
