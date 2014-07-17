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


class Notification(models.Model):
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    service_config = models.ForeignKey(ServiceConfiguration, related_name='notifications')

    # Fully qualified package name of the notification plugin.
    plugin = models.CharField(max_length=200)
    # Relation to plugin configuration.
    plugin_config = models.OneToOneField(NotificationPluginConfiguration, null=True, related_name='notification')

    name = models.CharField(max_length=100, help_text='Verbose name for this notification.')
    description = models.TextField(blank=True)

    on_ok = models.BooleanField(default=False, help_text='Send notification if service continues to be up. (SUBJECT TO OK interval')
    on_soft_critical = models.BooleanField(default=False, help_text='Send notification if service goes down soft.')
    on_soft_warning = models.BooleanField(default=False, help_text='Send notification if service continues to be down on retries (SOFT state).')
    on_soft_recovery = models.BooleanField(default=False, help_text='Send notification if service recovers from SOFT down.')
    on_hard_critical = models.BooleanField(default=True, help_text='Send notification if service goes down hard.')
    on_hard_warning = models.BooleanField(default=True, help_text='Send notification if service continues to be down (subject to interval_hard_warning).')
    on_hard_recovery = models.BooleanField(default=True, help_text='Send notification if service recovers from HARD down.')

    always_on_hard_recovery = models.BooleanField(default=True, help_text='Always send notification if service recovers (HARD)')

    interval = models.PositiveIntegerField(default=300, help_text=u'Notification interval in seconds.')
    interval_ok = models.PositiveIntegerField(default=0, help_text=u'Notification interval in seconds for service that stays up.')
    interval_hard_warning = models.PositiveIntegerField(default=3600, help_text=u'Notification interval in seconds for service that stays DOWN (hard).')

    last_sent = models.DateTimeField(null=True)


    def get_plugin(self):
        """
        Return the plugin class for this service.
        """

        return get_cls_by_name(self.plugin)
