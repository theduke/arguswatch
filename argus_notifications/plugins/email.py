from django.db import models
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.conf import settings as django_settings

from django_baseline.forms import CrispyModelForm

from . import NotificationPlugin, NotificationPluginConfigurationError
from ..models import NotificationPluginConfiguration


class EmailPluginConfig(NotificationPluginConfiguration):
    emails = models.TextField(verbose_name='Multiple Email addresses you want to send to. Separated by semicolon (;).')
    subject = models.CharField(max_length=255, verbose_name='Email subject (Will be appended with service name and state)', blank=True)
    message = models.TextField('Email message body. Will be appended with service, state and description', blank=True)


    class Meta:
        verbose_name = _('EmailPluginConfig')
        verbose_name_plural = _('EmailPluginConfigs')
        app_label = "argus_notifications"


    def get_settings(self):
        return {
            'emails': self.emails,
            'subject': self.subject,
            'message': self.message
        }

class EmailPluginForm(CrispyModelForm):
    class Meta:
        model = EmailPluginConfig
        fields = ['emails', 'subject', 'message']


class EmailNotification(NotificationPlugin):
    name = "Email"
    description = "Send Email."
    config_class = EmailPluginConfig
    form_class = EmailPluginForm


    def do_notify(self, settings, service_data, event, old_service_data=None):
        subject, message = self.build_subject_and_message(service_data, event)

        recipients = settings['emails'].split(';')
        subject = settings['subject'] + ' ' + subject
        message = settings['message'] + '\n' + message

        if not hasattr(django_settings, 'SERVER_EMAIL'):
            raise NotificationPluginConfigurationError('SERVER_EMAIL not configured, and no sender email set')
        from_email = django_settings.SERVER_EMAIL

        send_mail(subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipients,
        )
