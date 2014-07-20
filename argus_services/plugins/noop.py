from django.db import models
from django.utils.translation import ugettext as _

from django_baseline.forms import CrispyModelForm

from . import ServicePlugin, ServiceIsDownException, PluginCheckError
from ..models import ServicePluginConfiguration


class NoOpPluginConfig(ServicePluginConfiguration):

    def get_settings(self):
        return {}


    class Meta:
        verbose_name = _('NoOpPluginConfig')
        verbose_name_plural = _('NoOpPluginConfigs')
        app_label = "argus_services"


class NoOpPluginForm(CrispyModelForm):
    class Meta:
        model = NoOpPluginConfig
        fields = []


class NoOpService(ServicePlugin):
    name = "NoOp"
    description = "Do nothing. Used for Services that are updated externally via the API."
    is_passive = True
    config_class = NoOpPluginConfig
    form_class = NoOpPluginForm


    def run_check(self, settings):
        pass
