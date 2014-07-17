from django.db import models
from django.utils.translation import ugettext as _

from django_baseline.forms import CrispyModelForm

from . import ServicePlugin
from ..models import ServicePluginConfiguration


class HttpPluginConfig(ServicePluginConfiguration):
    url = models.URLField(max_length=500)

    timeout = models.IntegerField(default=30, help_text='Time allowed for server to respond')
    response_code = models.IntegerField(default=200, help_text='Expected HTTP response code (200 is the default OK).')
    response_text = models.TextField(blank=True, help_text='OPTIONAL expected (TRIMMED!) http response body.')


    class Meta:
        verbose_name = _('HttpPluginConfig')
        verbose_name_plural = _('HttpPluginConfigs')
        app_label = "arguswatch"
 


class HttpPluginForm(CrispyModelForm):
    class Meta:
        model = HttpPluginConfig
        fields = ['url', 'timeout', 'response_code', 'response_text']


class HttpService(ServicePlugin):
    name = "HTTP"
    description = "Check if a website is reachable."
    config_class = HttpPluginConfig
    form_class = HttpPluginForm
