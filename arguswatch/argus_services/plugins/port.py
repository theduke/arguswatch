from django.db import models
from django.utils.translation import ugettext as _

from django_baseline.forms import CrispyModelForm

from . import ServicePlugin, ServiceIsDown, PluginCheckError
from ..models import ServicePluginConfiguration


class PortPluginConfig(ServicePluginConfiguration):
    host = models.CharField(max_length=255)
    port = models.PositiveIntegerField(default=80)
    timeout = models.IntegerField(default=10, help_text='Time allowed for server to respond')

    def get_settings(self):
        return {
            'host': self.host,
            'port': self.port,
            'timeout': self.timeout,
        }


    class Meta:
        verbose_name = _('PortPluginConfig')
        verbose_name_plural = _('PortPluginConfigs')
        app_label = "argus_services"
 


class PortPluginForm(CrispyModelForm):
    class Meta:
        model = PortPluginConfig
        fields = ['host', 'port', 'timeout']


class PortService(ServicePlugin):
    name = "Port"
    description = "Check if a server port is open and accepting connections."
    is_passive = False
    config_class = PortPluginConfig
    form_class = PortPluginForm


    def run_check(self, settings):
        host = settings['host']
        port = settings['port']
        timeout = settings['timeout']

        log = self.get_logger()
        log.debug('Checking if {host} is accepting connections on port {port}'.format(
            host=host, port=port
        ))

        import socket;

        result = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
        except socket.gaierror as e:
            raise ServiceIsDown('DNS Lookup for {} failed.'.format(host))

        if result != 0:
            raise ServiceIsDown('Unreachable')
