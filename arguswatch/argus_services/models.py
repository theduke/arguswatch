import datetime
import logging
from io import StringIO

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey
from polymorphic import PolymorphicModel

from arguswatch.utils.django import get_cls_by_name
from arguswatch.argus_service_configurations.models import ServiceConfiguration


class ContactGroup(models.Model):

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _('ContactGroup')
        verbose_name_plural = _('ContactGroups')

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    group = models.ForeignKey(ContactGroup, null=True, blank=True, related_name='contacts')

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return self.name



class ServicePluginConfiguration(PolymorphicModel):
    """
    A base class that holds the configuration for a Plugin 
    for one individual service.
    """
    
    class Meta:
        pass

    def __str__(self):
        return self.__class__.__name__


from .plugins.http import HttpPluginConfig
from .plugins.ping import PingPluginConfig
from .plugins.port import PortPluginConfig
from .plugins.noop import NoOpPluginConfig
from .plugins.sql_query import SQLQueryPluginConfig

from .plugins.smtp import SMTPPluginConfig
from .plugins.pop import POPPluginConfig
from .plugins.imap import IMAPPluginConfig

from .plugins.ssh import SSHPluginConfig
from .plugins.ssh_cmd import SSHCmdPluginConfig


class ServiceGroup(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    slug = models.SlugField(unique=True)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = _('ServiceGroup')
        verbose_name_plural = _('ServiceGroups')

    class MPTTMeta:
        order_insertion_by = ['name']


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ServiceGroup, self).save(*args, **kwargs)


class Service(models.Model):
    """
    As the centerpiece of ArgusWatch, a Service is a host or an actual service,
    that will be monitored.

    The state logic copied from from Nagios. See http://nagios.sourceforge.net/docs/3_0/statetypes.html.
    """

    #### Fields holding basic info. ####

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True, 
        verbose_name='Additional notes for further information')
    tags = TaggableManager(blank=True)

    slug = models.SlugField(unique=True)

    # Service parent. Important for check hierarchy.
    parent = models.ForeignKey('Service', null=True, blank=True,
        related_name='children')

    groups = models.ManyToManyField(ServiceGroup, null=True, blank=True, 
        related_name='services')

    #### Configuration fields. ####

    # Fully qualified package name of the plugin.
    plugin = models.CharField(max_length=200)
    # Relation to plugin configuration.
    plugin_config = models.ForeignKey(ServicePluginConfiguration, null=True, related_name='service')

    config = models.ForeignKey(ServiceConfiguration, 
        related_name='services', verbose_name='Service Template')

    enabled = models.BooleanField(default=True, 
        help_text='Disable to pause checks and notifications.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

    #### State related fields ###

    STATE_UNKNOWN = 'unknown'
    STATE_DOWN = 'down'
    STATE_WARNING = 'warning'
    STATE_OK = 'ok'

    STATE_CHOICES = (
        (STATE_UNKNOWN, 'unknown'),
        (STATE_DOWN, 'down'),
        (STATE_WARNING, 'warning'),
        (STATE_OK, 'ok'),
    )

    # Current event state.
    state = models.CharField(max_length=20, choices=STATE_CHOICES, 
        default=STATE_UNKNOWN)
    # Wether state is provisional.
    # State will stay provisional, until a number of rechecks have been 
    # executed. The amount is determined by config.
    state_provisional = models.BooleanField(default=False)
    # Message specifying state. Most important for warning.
    state_message = models.TextField(blank=True)

    # The last time a check was issued.
    last_issued = models.DateTimeField(null=True)
    # The celery task id of the currently active check. Null if no check is running.
    celery_task_id = models.CharField(max_length=100, blank=True, default='')

    # The last time a check for this service finished.
    last_checked = models.DateTimeField(null=True)
    # The last time this service was reported as ok.
    last_ok = models.DateTimeField(null=True)
    # Last time this service changed state.
    last_state_change = models.DateTimeField(null=True)

    # The number of retries that have been executed for this service.
    # Important to switch from provisional to hard states.
    num_retries = models.PositiveSmallIntegerField(default=0)


    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

        permissions = (
            ("view_service", "Can view service"),
            ("run_service_check", "Can run service check"),
            ("issue_service_check", "Can issue service check"),
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ServiceSTATE_UNKNOWN_PROVISIONAL, self).save(*args, **kwargs)

    def to_dict(self):
        """
        Convert to a dictionary, with the most important fields.
        """
        return {
            'name': self.name,
            'description': self.description,
            'state_type': self.state_type,
            'state': self.state,
            'last_ok': self.last_ok,
            'last_state_change': self.last_state_change,
            'num_retries': self.num_retries
        }

    def get_plugin(self):
        """
        Return the plugin class for this service.
        """

        return get_cls_by_name(self.plugin)

    def get_plugin_name(self):
        """
        Get the pretty plugin name.
        """

        return self.get_plugin().name

    def issue_check(self, run_locally=False):
        if self.celery_task_id:
            raise Exception("Another check is already in progress.")

        from arguswatch.celery import checker

        result = None
        result_data = None

        if run_locally:
            # Build up a string logger to be able to return the log results.
            logger = logging.getLogger('django.argus.celery')
            logger.setLevel(logging.DEBUG)
            # Handler.
            stream = StringIO()
            handler = logging.StreamHandler(stream)
            handler.setLevel(logging.DEBUG)
            # Formatter.
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            
            for handler in logger.handlers:
                logger.removeHandler(handler)
            logger.addHandler(handler)

            result = checker.apply((self.plugin, 
                self.plugin_config.get_settings()), {'logger': logger})
            result_data = self.handle_check_result(result, log=logger)

            # Flush logging handler to ensure all logs are written to streamIO stream.
            handler.flush()
            result_data['logs'] = stream.getvalue()
            stream.close()
        else:
            result = checker.delay(self.plugin, self.plugin_config.get_settings()) 
            self.celery_task_id = result.id

        self.last_issued = timezone.now()
        self.save()

        return result_data if run_locally else result

    def issue_passive_check(self, data, run_locally=True):
        # TODO: IMPLEMENT!
        raise Exception("Not implemented")

    def handle_check_result(self, result, log=None):
        """
        Handle the check result from a service check done by a service plugin
        by determining which event should be triggered for the service state
        that was determined by the check, and then properly process the event
        to change service state and send the appropriate notifications.

        The result is a celery task result object
        """

        if not log:
            log = logging.getLogger('django.argus')

        # Retrieve data from task result.
        state, message = result.get()

        # Build an Event instance.
        event = self.determine_event(state, message)
        log.debug("Determined event for service {}: {}".format(self, event.event))

        # Update last_checked and celery task id.
        # Service is persisted in process_event().
        self.last_checked = timezone.now()
        self.celery_task_id = ''

        # Process event.
        self.process_event(event)

        return {
            'state': state,
            'message': message,
            'event': event,
        }

    def determine_appropriate_check_interval(self):
        """
        Based on the current state of the service,
        determine which config interval should be used.
        Available: check_interval, retry_interval_soft, retry_interval_hard.
        """

        config = self.config
        state = self.state
        interval = None

        if self.state_provisional:
            # State is provisional, so use provisional interval.
            interval = selfconfig.check_interval_provisional
        else:
            # State is locked (not provisional).
            # Each state has a custom interval, so 
            # use the appropriate one.
            if state == self.STATE_OK:
                interval = config.check_interval_ok
            elif state == self.STATE_WARNING:
                interval = config.check_interval_warning
            elif state == self.STATE_DOWN:
                interval = config.check_interval_down
            elif state == self.STATE_UNKNOWN:
                interval = config.check_interval_unknown

        return interval

    def is_check_needed(self):
        """
        Determine, if a new check needs to be issued right now,
        based on service configuration.
        """

        # For passive plugins, check is never needed.
        if self.get_plugin().is_passive:
            return False

        # If no check was run before (true for newly added services), then 
        # a check is always needed.
        if not self.last_checked:
            return True

        interval = self.determine_appropriate_check_interval()
        delta = datetime.timedelta(seconds=interval)
        
        if timezone.now() - self.last_checked >= delta:
            # Enough time has passed, new check is needed.
            return True
        else:
            # Nothing needs to be done.
            return False

    def determine_event(self, state, message):
        """
        Determine the event that needs to be triggered based on the 
        current state of the service, as determined by a service plugin 
        check.

        Returns an Event instance.
        """

        # For readability!
        old_state = self.state
        was_provisional = self.state_provisional

        max_retries = self.config.max_retries
        retries = self.num_retries + 1

        event = None

        if state == self.STATE_OK:
            # Service IS OK now.
            
            if old_state == self.STATE_OK:
                # Stays OK.
                event = Event.EVENT_STAYS_OK

            else:
                # Service was NOT OK before, so trigger GOES_OK event.
                event = Event.EVENT_GOES_OK
               
        elif state == self.STATE_WARNING:
            # Service is in state WARNING now.

            if old_state == self.STATE_WARNING:
                # Was already in warning.
                event = Event.EVENT_STAYS_WARNING
            else:
                # Goes to state warning.
                event = Event.EVENT_GOES_WARNING
        elif state == self.STATE_DOWN:
            # Service is DOWN now.

            if old_state == self.STATE_DOWN:
                # Service was already down.
                # If state was provisionally down, check if maximum retries
                # have been reached. If so, state is no longer provisional.

                if was_provisional:
                    if retries >= max_retries:
                        # Was provisional, but max_retries have been reached,
                        # so state locks in as down.
                        event = Event.EVENT_GOES_DOWN
                    else:
                        # Have not reached max_retries yet, so remain down 
                        # provisionally.
                        event = Event.EVENT_STAYS_DOWN_PROVISIONAL
                else:
                    # Was locked as down and stays that way.
                    event = Event.EVENT_STAYS_DOWN
            else:
                # Service is down now, but was not before.

                if max_retries < 1:
                    # No retries allowed, so the provisional down state is skipped
                    # and service goes straight to down.
                    event = Event.EVENT_GOES_DOWN
                else:
                    # Retries allowed, so go to provisional down.
                    event = Event.EVENT_GOES_DOWN_PROVISIONAL
        elif state == self.STATE_UNKNOWN:
            # Service is UNKNOWN now.

            if old_state == self.STATE_UNKNOWN:
                # Service was already unknown.
                # If state was provisionally unknown, check if maximum retries
                # have been reached. If so, state is no longer provisional.

                if was_provisional:
                    if retries >= max_retries:
                        # Was provisional, but max_retries have been reached,
                        # so state locks in as unknown.
                        event = Event.EVENT_GOES_UNKNOWN
                    else:
                        # Have not reached max_retries yet, so remain unknown 
                        # provisionally.
                        event = Event.EVENT_STAYS_UNKNOWN_PROVISIONAL
                else:
                    # Was locked as unknown and stays that way.
                    event = Event.EVENT_STAYS_UNKNOWN
            else:
                # Service is unknown now, but was not before.

                if max_retries < 1:
                    # No retries allowed, so the provisional unknown state is skipped
                    # and service goes straight to unknown.
                    event = Event.EVENT_GOES_UNKNOWN
                else:
                    # Retries allowed, so go to provisional unknown.
                    event = Event.EVENT_GOES_UNKNOWN_PROVISIONAL

        # Determine if new state is provisional.
        is_provisional = event in (
            Event.EVENT_GOES_DOWN_PROVISIONAL,
            Event.EVENT_STAYS_DOWN_PROVISIONAL,
            Event.EVENT_GOES_UNKNOWN_PROVISIONAL,
            Event.EVENT_STAYS_UNKNOWN_PROVISIONAL,
        )

        instance = Event(
            old_state=state, old_state_provisional=was_provisional
            new_state=state, new_state_provisional=is_provisional,
            event=event,
            message=message or '',
            time=timezone.now()
        )

        return instance

    def trigger_event(self, event):
        """
        Adapt the state of this event based on an Event instance.

        DOES NOT persist service.
        Persistence is handled by process_event.

        Returns Event instance describing the event.
        """

        now = event.time

        kind = event.event

        # Set new state and provisional state.
        self.state = event.new_state
        self.provisional = event.new_state_provisional

        # If state was provisional, but is not provisional anymore,
        # retry counter must be reset to 0.
        if event.old_state_provisional and not event.new_state_provisional:
            self.num_retries = 0

        # If state has changed, update last_state_change.
        if event.old_state != event.new_state:
            self.last_state_change = now

        # If service is OK now, update last_ok.
        if event.new_state == self.STATE_OK:
            self.last_ok = now


    def determine_notifications_to_send(self, event):
        """
        Determine which notifications should be sent for an event.
        """

        return [n for n in self.config.notifications.all() if n.should_notify(self, event)]

    def process_event(self, event):
        """
        Do the complete workflow that takes place, 
        when an event occurs.

        Includes the execution of trigger_event and persisting the service.

        event is an Event instance.
        """

        self.trigger_event(event)
        self.save()

        notifications = self.determine_notifications_to_send(event)

        for n in notifications:
            n. do_notify(self, event)

        # TODO: Event persistance.


class Event(models.Model):

    EVENT_GOES_UNKNOWN_PROVISIONAL = 'goes_unknown_provisional'
    EVENT_STAYS_UNKNOWN_PROVISIONAL = 'stays_unknown_provisional'
    EVENT_GOES_UNKNOWN = 'goes_unknown'
    EVENT_STAYS_UNKNOWN = 'stays_unknown'
    EVENT_GOES_DOWN_PROVISIONAL = 'goes_down_provisional'
    EVENT_STAYS_DOWN_PROVISIONAL = 'goes_down'
    EVENT_GOES_DOWN = 'goes_down'
    EVENT_STAYS_DOWN = 'stays_down'
    EVENT_GOES_WARNING = 'goes_warning'
    EVENT_STAYS_WARNING = 'stays_warning'
    EVENT_GOES_OK = 'goes_ok'
    EVENT_STAYS_OK = 'stays_ok'

    EVENT_CHOICES = (
        (EVENT_GOES_UNKNOWN, 'goes_unknown'), 
        (EVENT_STAYS_UNKNOWN, 'stays_unknown'), 
        (EVENT_GOES_DOWN, 'goes_down'), 
        (EVENT_STAYS_DOWN, 'stays_down'), 
        (EVENT_GOES_WARNING, 'goes_warning'), 
        (EVENT_STAYS_WARNING, 'stays_warning'), 
        (EVENT_GOES_OK, 'goes_ok'), 
        (EVENT_STAYS_OK, 'stays_ok'), 
    )

    old_state = models.CharField(max_length=20, choices=Service.STATE_CHOICES)
    old_state_provisional = models.BooleanField()

    new_state = models.CharField(max_length=20, choices=Service.STATE_CHOICES)
    new_state_provisional = models.BooleanField()

    event = models.CharField(max_length=20, choices=EVENT_CHOICES)
    message = models.TextField(blank=True)

    time = models.DateTimeField()
