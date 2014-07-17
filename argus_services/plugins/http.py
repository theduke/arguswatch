from django.db import models
from django.utils.translation import ugettext as _

from django_baseline.forms import CrispyModelForm

from . import ServicePlugin, ServiceIsDownException, PluginCheckError
from ..models import ServicePluginConfiguration


class HttpPluginConfig(ServicePluginConfiguration):
    url = models.URLField(max_length=500)

    timeout = models.IntegerField(default=30, help_text='Time allowed for server to respond')
    response_code = models.IntegerField(default=200, help_text='Expected HTTP response code (200 is the default OK).')
    response_text = models.TextField(blank=True, help_text='OPTIONAL expected (TRIMMED!) http response body.')


    def get_settings(self):
        return {
            'url': self.url,
            'timeout': self.timeout,
            'response_code': self.response_code,
            'response_text': self.response_text
        }


    class Meta:
        verbose_name = _('HttpPluginConfig')
        verbose_name_plural = _('HttpPluginConfigs')
        app_label = "argus_services"
 


class HttpPluginForm(CrispyModelForm):
    class Meta:
        model = HttpPluginConfig
        fields = ['url', 'timeout', 'response_code', 'response_text']


class HttpService(ServicePlugin):
    name = "HTTP"
    description = "Check if a website is reachable."
    config_class = HttpPluginConfig
    form_class = HttpPluginForm


    def run_check(self, settings):
        log = self.get_logger()

        import urllib.request

        result = None

        log.debug("Checking " + settings['url'])

        try:
            result = urllib.request.urlopen(settings['url'], timeout=settings['timeout'])
        except urllib.request.URLError as e:
            raise ServiceIsDownException('Unreachable')

        if settings['response_code'] != result.getcode():
            raise ServiceIsDownException('Wrong HTTP Code: {} (expected: {}'.format(
                result.getcode(), settings['response_code']))

        if settings['response_text']:
            if settings['response_text'] != result.read().trim():
                raise ServiceIsDownException('HTML Response body did not match')
