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
    notes = models.TextField(blank=True, verbose_name='Additional notes for further information')
    tags = TaggableManager(blank=True)

    slug = models.SlugField(unique=True)

    # Service parent. Important for check hierarchy.
    parent = models.ForeignKey('Service', null=True, blank=True, related_name='children')

    groups = models.ManyToManyField(ServiceGroup, null=True, blank=True, related_name='services')

    #### Configuration fields. ####

    # Fully qualified package name of the plugin.
    plugin = models.CharField(max_length=200)
    # Relation to plugin configuration.
    plugin_config = models.ForeignKey(ServicePluginConfiguration, null=True, related_name='service')

    service_config = models.ForeignKey(ServiceConfiguration, related_name='services', verbose_name=u'Service Template')

    enabled = models.BooleanField(default=True, help_text='Disable to pause checks and notifications for this service.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

    #### State related fields ###

    STATE_TYPE_SOFT = 1
    STATE_TYPE_HARD = 2

    STATE_TYPE_CHOICES = (
        (STATE_TYPE_SOFT, 'soft'),
        (STATE_TYPE_HARD, 'hard'),
    )

    STATE_UNKNOWN = 0
    STATE_OK = 1
    STATE_WARNING = 2
    STATE_CRITICAL = 3

    STATE_CHOICES = (
        STATE_OK, 'ok',
        STATE_WARNING, 'warning',
        STATE_CRITICAL, 'critical',
    ) 

    CHECK_STATE_UP = "up"
    CHECK_STATE_DOWN = "down"
    CHECK_STATE_KNOWN_ERROR = "known_error"
    CHECK_STATE_UNKNOWN_ERROR = "unknown_error"

    EVENT_RECOVERY_SOFT = 'recovery_soft'
    EVENT_RECOVERY_HARD = 'recovery_hard'
    EVENT_CRITICAL_SOFT = 'critical_soft'
    EVENT_CRITICAL_HARD = 'critical_hard'
    EVENT_WARNING_SOFT = 'warning_soft'
    EVENT_WARNING_HARD = 'warning_hard'
    EVENT_REMAINS_UP = 'remains_up'

    EVENTS = (
        EVENT_RECOVERY_SOFT,
        EVENT_RECOVERY_HARD,
        EVENT_CRITICAL_SOFT,
        EVENT_CRITICAL_HARD,
        EVENT_WARNING_SOFT,
        EVENT_WARNING_HARD,
        EVENT_REMAINS_UP,
    )

    state_type = models.PositiveSmallIntegerField(default=STATE_TYPE_HARD)
    state = models.PositiveSmallIntegerField(default=STATE_UNKNOWN)

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
    num_retries = models.PositiveSmallIntegerField(default=0)


    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Service, self).save(*args, **kwargs)


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


    def get_state_description(self):
        """
        Returns a usable "up", "down", "unknown" or "warning"
        """

        if self.state == self.STATE_UNKNOWN:
            return 'unknown'
        if self.state == self.STATE_OK:
            return "up"
        elif self.state_type == self.STATE_TYPE_SOFT:
            return "warning"
        elif self.state == self.STATE_CRITICAL:
            return "down"


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

            result = checker.apply((self.plugin, self.plugin_config.get_settings()), {'logger': logger})
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


    def handle_check_result(self, result, log=None):
        if not log:
            log = logging.getLogger('django.argus')

        state, message = result.get()

        # Event to trigger.
        event = None

        if state == Service.CHECK_STATE_UP or state == Service.CHECK_STATE_DOWN:
            event = self.determine_event(state)
            log.debug("Determined event for service {}: {}".format(self, event))
            self.process_event(event, message)
        elif state == Service.CHECK_STATE_KNOWN_ERROR:
            # TODO: handle with retry.
            pass
        elif state == Service.CHECK_STATE_UNKNOWN_ERROR:
            # TODO: handle with retry.
            pass

        return {
            'state': state,
            'message': message,
            'event': event,
        }


    def issue_passive_check(self, data, run_locally=True):
        # TODO: implement celery execution of passive checks.
        event = self.get_plugin()().on_data_received(data)
        if event:
            self.process_event(event)


    def determine_appropriate_check_interval(self):
        """
        Based on the current state and state type of the service,
        determine which config interval should be used.
        Available: check_interval, retry_interval_soft, retry_interval_hard.
        """

        interval = None

        if self.state == Service.STATE_OK:
            # State is OK.
            # Relevant interval is the check_interval.
            interval = self.service_config.check_interval
        elif self.state_type == Service.STATE_TYPE_SOFT:
            # State type is SOFT.
            # Reagardless whether state is critical or warning,
            # the relevant interval is retry_interval_soft
           interval = self.service_config.retry_interval_soft
        elif self.state_type == Service.STATE_TYPE_HARD:
            # State type is HARD.
            # HARD means OK, which is handled by the first if branch,
            # or CRITICAL/WARNING.
            # Similar to the second branch for SOFT, the relevant interval
            # for this case is retry_interval_hard.
            
           interval = self.service_config.retry_interval_hard

        return interval


    def is_check_needed(self):
        """
        Determine, if a new check needs to be issued right now.
        """

        # For passive plugins, check is never needed.
        if self.get_plugin().is_passive:
            return False

        # Always need to check if no last_check time is set.
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


    def determine_event(self, state):
        # For readability!
        was_up = self.state == self.STATE_OK
        was_down = not was_up


        evt = None

        if state == self.CHECK_STATE_UP:
            # Service IS UP now.
            
            if was_down:
                # Service WAS DOWN before, so trigger recovery event.
                if self.state_type == self.STATE_TYPE_SOFT:
                    # Soft recovery.
                    evt = self.EVENT_RECOVERY_SOFT
                else:
                    # Hard recovery.
                    evt = self.EVENT_RECOVERY_HARD
            else:
                evt = self.EVENT_REMAINS_UP
        elif state == self.CHECK_STATE_DOWN:
            # Service IS DOWN now.
            
            if was_up:
                # Service WAS UP before. 
                # Trigger critical soft event.
                evt = self.EVENT_CRITICAL_SOFT
            elif was_down:
                # Service WAS alread DOWN.
                
                # Handle SOFT and HARD state separately.
                if self.state_type == self.STATE_TYPE_SOFT:
                    # Event type IS SOFT. 
                    # We remain in SOFT, until max_retries_soft is reached.
                    
                    try_index = self.num_retries + 1
                    if try_index < self.service_config.max_retries_soft:
                        # Still retries left, so just issue SOFT WARNING.
                        evt = self.EVENT_WARNING_SOFT
                    else:
                        # Maximum retries reached, so issue a HARD CRITICAL.
                        evt = self.EVENT_CRITICAL_HARD
                else:
                    # Event type is HARD.
                    # Issue HARD WARNING.
                    evt = self.EVENT_WARNING_HARD

        return evt


    def determine_notifications_to_send(self, event):
        """
        Determine which notifications should be sent for an event.
        """

        return [n for n in self.service_config.notifications.all() if n.should_send(self, event)]


    def process_event(self, event, message):
        """
        Do the complete workflow that takes place, 
        when an event occurs.

        Includes the executio of trigger_event.
        """

        self.trigger_event(event)
        self.last_checked = timezone.now()

        self.celery_task_id = ''
        self.save()

        notifications = self.determine_notifications_to_send(event)

        for n in notifications:
            n. do_notify(self, event)


    def trigger_event(self, event):
        """
        Adapt the state of this event based on an event type.
        Note that the 1st argument event is one of self.CHECK_STATE_*.

        DOES NOT persist service.
        Persistence is handled by process_event
        """

        now = timezone.now()

        if event == self.EVENT_RECOVERY_HARD:
            # Service WAS down (HARD) and CAME UP.
            self.state_type = self.STATE_TYPE_HARD
            self.state = self.STATE_OK
            self.num_retries = 0
            self.last_ok = now
            self.last_state_change = now
        elif event == self.EVENT_RECOVERY_SOFT:
            # Service WAS down (SOFT) and CAME UP.
            self.state_type = self.STATE_TYPE_HARD
            self.state = self.STATE_OK
            self.num_retries = 0
            self.last_ok = now
            self.last_state_change = now
        elif event == self.EVENT_WARNING_HARD:
            # Service WAS down (HARD) and IS STILL down.
            self.state = self.STATE_WARNING
        elif event == self.EVENT_WARNING_SOFT:
            # Service WAS down (SOFT) and IS STILL down.
            # max retries have not been reached yet.
            # Just increment the counter.
            self.state = self.STATE_WARNING
            self.num_retries += 1
        elif event == self.EVENT_CRITICAL_HARD:
            # Service WAS DOWN (SOFT) and is now DOWN (HARD).
            self.state_type = self.STATE_TYPE_HARD
            self.state = self.STATE_CRITICAL
            self.num_retries = 0
            self.last_state_change = now
        elif event == self.EVENT_CRITICAL_SOFT:
            # Service WAS UP and went DOWN.
            self.state_type = self.STATE_TYPE_SOFT
            self.state = self.STATE_WARNING
            self.last_state_change = now
        elif event == self.EVENT_REMAINS_UP:
            self.last_ok = now
        else:
            raise Exception("Unknown Service event: " + event)
