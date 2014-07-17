from django.db import models
from django.utils.translation import ugettext as _

from polymorphic import PolymorphicModel

from arguswatch.utils.django import get_cls_by_name
from arguswatch.services.models import ServiceConfiguration


class NotificationPluginConfiguration(PolymorphicModel):
    """
    A base class that holds the configuration for a Plugin 
    for one individual notification.
    """
    
    class Meta:
        app_label = "arguswatch"


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


    def get_plugin(self):
        """
        Return the plugin class for this service.
        """

        return get_cls_by_name(self.plugin)
