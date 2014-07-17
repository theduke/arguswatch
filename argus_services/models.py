import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
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

    # Service parent. Important for check hierarchy.
    parent = models.ForeignKey('Service', null=True, blank=True, related_name='children')

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

    STATE_OK = 1
    STATE_WARNING = 2
    STATE_CRITICAL = 3

    STATE_CHOICES = (
        STATE_OK, 'ok',
        STATE_WARNING, 'warning',
        STATE_CRITICAL, 'critical',
    ) 

    state_type = models.PositiveSmallIntegerField(default=STATE_TYPE_HARD)
    state = models.PositiveSmallIntegerField(default=STATE_OK)

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


    def get_plugin(self):
        """
        Return the plugin class for this service.
        """

        return get_cls_by_name(self.plugin)


    def issue_check(self, run_locally=False):
        if self.celery_task_id:
            raise Exception("Another check is already in progress.")

        from arguswatch.celery import checker

        result = None
        result_data = None

        if run_locally:
            result = checker.apply((self.plugin, self.plugin_config.get_settings()))
            result_data = result.get()
        else:
            result = checker.delay(self.plugin, self.plugin_config.get_settings()) 
            self.celery_task_id = result.id

        self.last_issued = datetime.datetime.now()
        self.save()

        return result_data if run_locally else result


    def determine_appropriate_check_interval(self):
        """
        Based on the current state and state type of the service,
        determine which config interval should be used.
        Available: check_interval, retry_interval_soft, retry_interval_hard.
        """

        interval = None

        if self.STATE == Service.STATE_OK:
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

        # Always need to check if no last_check time is set.
        if not self.last_checked:
            return True

        interval = self.determine_appropriate_check_interval()
        delta = datetime.timedelta(seconds=interval)
        
        if datetime.datetime.now() - self.last_checked >= delta:
            # Enough time has passed, new check is needed.
            return True
        else:
            # Nothing needs to be done.
            return False
