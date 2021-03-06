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
    config = models.ForeignKey(ServiceConfiguration, related_name='notifications')

    # Fully qualified package name of the notification plugin.
    plugin = models.CharField(max_length=200)
    # Relation to plugin configuration.
    plugin_config = models.ForeignKey(NotificationPluginConfiguration, null=True, related_name='notification')

    name = models.CharField(max_length=100, help_text='Verbose name for this notification.')
    description = models.TextField(blank=True)

    # Intervals for different types of events.
    # The last time each time was sent is persisted in the 
    # NotificationHistory object as last_*.

    interval_state_change_provisional = models.SmallIntegerField(default=-1,
        help_text='Interval in seconds for service entering a provisional state (either UNKNOWN or DOWN).')
    interval_state_stays_provisional = models.SmallIntegerField(default=-1,
        help_text='Interval in seconds for service remaining in a provisional state (either UNKNOWN or DOWN).')
    interval_state_change = models.SmallIntegerField(default=60,
        help_text='Interval in seconds for service entering a non-provisional state (UNKNOWN, DOWN, WARNING).')
    interval_state_stays = models.SmallIntegerField(default=60*60*12,
        help_text='Interval in seconds for service remaining in non-provisional state (UNKNOWN, DOWN, WARNING).')
    interval_stays_ok = models.SmallIntegerField(default=-1,
        help_text='Interval in seconds for service remaining OK.')
    interval_change_ok = models.SmallIntegerField(default=0,
        help_text='Interval in seconds for service entering OR leaving state OK.')

    interval_hard = models.PositiveSmallIntegerField(default=5)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')


    def get_interval_field_for_event(self, event):
        event_stays = event.old_state == event.new_state
        provisional_stays = event.old_state_provisional == event.new_state_provisional

         # OK intervals overwrites defaults.
        if event.old_state == Service.STATE_OK and event.new_state == Service.STATE_OK:
            # stays_ok interval is responsible if state stays OK.
            return 'interval_stays_ok'
        elif event.new_state == Service.STATE_OK or event.old_state == Service.STATE_OK:
            # State changed from OK or to OK.
            return 'interval_change_ok'

        if event_stays and provisional_stays:
            if event.new_state_provisional:
                return 'interval_state_stays_provisional'
            else:
                return 'interval_state_stays'
        else:
            if event.new_state_provisional:
                return 'interval_state_change_provisional'
            else:
                return 'interval_state_change'

    def get_interval_for_event(self, event):
        """
        Determine the interval in seconds to use for an event.
        """

        field = self.get_interval_field_for_event(event)
        return getattr(self, field)

    def get_last_sent_field_for_event(self, event):
        """
        Get the field responsible for the delta for a specific event.
        """

        # Reuse logic from interval field determination.
        field = self.get_interval_field_for_event(event).replace('interval_', 'last_')

        # For interval_stays_ok, the last_sent field is used.
        # Otherwise, the customly named field is.
        return field if field != 'last_stays_ok' else 'last_sent'

    def get_last_sent_for_event(self, event, history):
        """
        Get a DateTime for the last time a notification 
        for a speicic event kind was sent.
        """

        return getattr(history, self.get_last_sent_field_for_event(event))

    def should_notify(self, service, event):
        """
        Determine if notification should be sent for an event.
        """

        history = self.get_history_for_service(service)

        last_sent_hard = history.last_sent
        last_sent = None

        now = timezone.now()

        delta = self.get_interval_for_event(event)
        delta_hard = timedelta(seconds=self.interval_hard)
       
        last_sent = self.get_last_sent_for_event(event, history)
       
        if delta >= 0:
            # Notifications for this event are enabled.
            # Check time constraints.

            if not last_sent:
                # Notifications for this event are enabled,
                # and nothing has been sent yet, so definitely send.
                return True
            else:
                # Compare time passed to delta, and return 
                # if more time than delta has passed.
                should_send = now - last_sent >= timedelta(seconds=delta)

                if should_send:
                    # Sending is enabled, based on soft limits (for same
                    # notification type.
                    # Now check hard limit.

                    if now - last_sent_hard >= delta_hard:
                        return True
                    else:
                        return False
                else:
                    return False

    def get_history_for_service(self, service):
        """
        Return the NotificationHistory object for this notification and
        a service.
        If none exists yet, a new one is created.
        """

        history = self.histories.filter(service=service).first()\
          or NotificationHistory(notification=self, service=service)

        return history

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

    def do_notify(self, service, event):
        plugin = self.get_plugin()()
        plugin.do_notify(self.get_plugin_settings(), service.to_dict(), event)

        history = self.get_history_for_service(service)
        now = timezone.now()

        # Update last_sent for specific notification type.
        field = self.get_last_sent_field_for_event(event)
        setattr(history, 'last_' + field, now)

        # Update general last_sent.
        history.last_sent = now

        # Persist.
        history.save()

    def __str__(self):
        return self.name


class NotificationHistory(models.Model):
    notification = models.ForeignKey(Notification, related_name='histories')
    service = models.ForeignKey(Service, related_name='notifications')

    last_sent = models.DateTimeField()
    last_state_change_provisional = models.DateTimeField(null=True)
    last_state_stays_provisional = models.DateTimeField(null=True)
    last_state_change = models.DateTimeField(null=True)
    last_state_stays = models.DateTimeField(null=True)
    last_change_ok = models.DateTimeField(null=True)

    class Meta:
        verbose_name = _('NotificationHistory')
        verbose_name_plural = _('NotificationHistories')
        unique_together = (('notification', 'service'),)
