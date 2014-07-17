from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
from polymorphic import PolymorphicModel

from arguswatch.utils.django import get_cls_by_name


class ContactGroup(models.Model):

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _('ContactGroup')
        verbose_name_plural = _('ContactGroups')
        app_label = "arguswatch"

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    group = models.ForeignKey(ContactGroup, null=True, blank=True, related_name='contacts')

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
        app_label = "arguswatch"

    def __str__(self):
        return self.name
    

class ServicePluginConfiguration(PolymorphicModel):
    """
    A base class that holds the configuration for a Plugin 
    for one individual service.
    """
    
    class Meta:
        app_label = "arguswatch"


    def __str__(self):
        return self.__class__.__name__


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
    plugin_config = models.OneToOneField(ServicePluginConfiguration, null=True, related_name='service')

    service_config = models.ForeignKey(ServiceConfiguration, related_name='services')

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
        app_label = "arguswatch"

    def __str__(self):
        return self.name


    def get_plugin(self):
        """
        Return the plugin class for this service.
        """

        return get_cls_by_name(self.plugin)

