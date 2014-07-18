from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone

from polymorphic import PolymorphicModel

from arguswatch.utils.django import get_cls_by_name
from arguswatch.argus_services.models import ServiceConfiguration, Service



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

    interval = models.PositiveIntegerField(default=60*30, help_text=u'Notification interval in seconds.')
    interval_remains_up = models.PositiveIntegerField(default=60*60*24, help_text=u'Notification interval in seconds for service that stays up.')
    interval_warning_hard = models.PositiveIntegerField(default=60*60, help_text=u'Notification interval in seconds for service that stays DOWN (hard).')
    interval_critical_hard = models.PositiveIntegerField(default=10*60, help_text=u'Notification interval in seconds for service that GOES DOWN (hard).')
    interval_recovery_hard = models.PositiveIntegerField(default=10*60, help_text=u'Notification interval in seconds for service that COMES UP (hard).')


    def should_send(self, service, evt):
        """
        Determine if notification should be sent for an event.
        """

        now = timezone.now()
        delta = None

        if evt == Service.EVENT_REMAINS_UP:
            if self.on_remains_up:
                delta = self.interval_remains_up
        elif evt == Service.EVENT_CRITICAL_SOFT:
            if self.on_critical_soft:
                delta = self.interval
        elif evt == Service.EVENT_WARNING_SOFT:
            if self.on_warning_soft:
                delta = self.interval
        elif evt == Service.EVENT_RECOVERY_SOFT:
            if self.on_recovery_soft:
                delta = self.interval
        elif evt == Service.EVENT_CRITICAL_HARD:
            if self.on_critical_hard:
                delta = self.interval_critical_hard
        elif evt == Service.EVENT_WARNING_HARD:
            if self.on_warning_hard:
                delta = self.interval_warning_hard
        elif evt == Service.EVENT_RECOVERY_HARD:
            if self.on_recovery_hard:
                delta = self.interval_recovery_hard

        # Determine last sent for service.
        sent_data = self.service_notifications.filter(service=service).first()
        last_sent = sent_data.last_sent if sent_data else None

        if delta:
            # Notifications for this event are enabled.
            # Check time constraints.

            if not last_sent:
                # Notifications for this event are enabled,
                # and nothing has been sent yet, so definitely send.
                return True
            else:
                # Compare time passed to delta, and return 
                # if more time than delta has passed.
                return now - last_sent >= timedelta(seconds=delta)


    def get_plugin(self):
        """
        Return the plugin class for this service.
        """

        return get_cls_by_name(self.plugin)


    def get_plugin_settings(self):
        """
        Retrieve the settings configured for the plugin
        as  a dict. 
        The plugin config s get_settings() is used.
        """

        return self.plugin_config.get_settings()


    def do_notify(self, service, event, old_service_data=None):
        plugin = self.get_plugin()()
        plugin.do_notify(self.get_plugin_settings(), service.to_dict(), event, old_service_data)

        sent_data = self.service_notifications.filter(service=service).first() or \
                    ServiceNotifications(service=service, notification=self)

        sent_data.last_sent = timezone.now()
        sent_data.save()


    def __str__(self):
        return self.name


class ServiceNotifications(models.Model):
    notification = models.ForeignKey(Notification, related_name='service_notifications')
    service = models.ForeignKey(Service, related_name='service_notifications')
    last_sent = models.DateTimeField()

    class Meta:
        verbose_name = _('ServiceNotifications')
        verbose_name_plural = _('ServiceNotificationss')
        unique_together = (('notification', 'service'),)
