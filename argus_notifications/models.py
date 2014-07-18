from django.db import models
from django.utils.translation import ugettext as _

from polymorphic import PolymorphicModel

from arguswatch.utils.django import get_cls_by_name
from arguswatch.argus_services.models import ServiceConfiguration


class NotificationPluginConfiguration(PolymorphicModel):
    """
    A base class that holds the configuration for a Plugin 
    for one individual notification.
    """
    
    class Meta:
        pass


    def __str__(self):
        return self.__class__.__name__

# Include plugins
from .plugins.email import EmailPluginConfig


class Notification(models.Model):
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    service_config = models.ForeignKey(ServiceConfiguration, related_name='notifications')

    # Fully qualified package name of the notification plugin.
    plugin = models.CharField(max_length=200)
    # Relation to plugin configuration.
    plugin_config = models.ForeignKey(NotificationPluginConfiguration, null=True, related_name='notification')

    name = models.CharField(max_length=100, help_text='Verbose name for this notification.')
    description = models.TextField(blank=True)

    # Service.EVENT_REMAINS_UP
    on_remains_up = models.BooleanField(default=False, help_text='Send notification if service continues to be up. (SUBJECT TO OK interval)')
    # Service.EVENT_CRITICAL_SOFT
    on_critical_soft = models.BooleanField(default=False, help_text='Send notification if service goes down soft.')
    # Service.EVENT_WARNING_SOFT
    on_warning_soft = models.BooleanField(default=False, help_text='Send notification if service continues to be down on retries (SOFT state).')
    # Service.EVENT_RECOVERY_SOFT
    on_recovery_soft = models.BooleanField(default=False, help_text='Send notification if service recovers from SOFT down.')
    # Service.EVENT_CRITICAL_HARD
    on_critical_hard = models.BooleanField(default=True, help_text='Send notification if service goes down hard.')
    # Service.EVENT_WARNING_HARD
    on_warning_hard = models.BooleanField(default=True, help_text='Send notification if service continues to be down (subject to interval_hard_warning).')
    # Service.EVENT_RECOVERY_HARD
    on_recovery_hard = models.BooleanField(default=True, help_text='Send notification if service recovers from HARD down.')

    always_on_recovery_hard = models.BooleanField(default=True, help_text='Always send notification if service recovers (HARD), even if interval would prevent it.')

    interval = models.PositiveIntegerField(default=300, help_text=u'Notification interval in seconds.')
    interval_ok = models.PositiveIntegerField(default=0, help_text=u'Notification interval in seconds for service that stays up.')
    interval_hard_warning = models.PositiveIntegerField(default=3600, help_text=u'Notification interval in seconds for service that stays DOWN (hard).')

    last_sent = models.DateTimeField(null=True)


    def get_plugin(self):
        """
        Return the plugin class for this service.
        """

        return get_cls_by_name(self.plugin)


    def __str__(self):
        return self.name


