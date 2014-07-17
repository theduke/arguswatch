import importlib

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
from polymorphic import PolymorphicModel

from .plugins import get_plugin_by_name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    parent = models.ForeignKey('Service', null=True, blank=True)

    tags = TaggableManager(blank=True)

    # Fully qualified package name of the plugin.
    plugin = models.CharField(max_length=200)
    # Relation to plugin configuration.
    config = models.ForeignKey('ServiceConfiguration', null=True)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)


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

        return get_plugin_by_name(self.plugin)



class ServiceConfiguration(PolymorphicModel):
    
    class Meta:
        app_label = "arguswatch"


    def __str__(self):
        return self.__class__.__name__
