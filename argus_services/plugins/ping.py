from django.db import models
from django.utils.translation import ugettext as _

from django_baseline.forms import CrispyModelForm
from django import forms

from . import ServicePlugin, ServiceIsDownException, PluginCheckError
from ..models import ServicePluginConfiguration


class PingPluginConfig(ServicePluginConfiguration):
    ip = models.IPAddressField(null=True, blank=True)
    domain  = models.CharField(max_length=255, blank=True)
    timeout = models.IntegerField(default=10, help_text='Time allowed for server to respond')
    cmd = models.TextField(blank=True, help_text='System command for executing the ping. Only change this IF NECCESSARY. If blank, default will be used. Default: "ping -c1 -w{timeout} {host}"')

    def get_settings(self):
        return {
            'host': self.ip or self.domain,
            'timeout': self.timeout,
            'cmd': self.cmd,
        }


    class Meta:
        verbose_name = _('PingPluginConfig')
        verbose_name_plural = _('PingPluginConfigs')
        app_label = "argus_services"


class PingPluginForm(CrispyModelForm):
    class Meta:
        model = PingPluginConfig
        fields = ['ip', 'domain', 'timeout']

    def clean(self):
        cleaned_data = super(PingPluginForm, self).clean()

        if not (cleaned_data.get('ip') or cleaned_data.get('domain')):
            raise forms.ValidationError('Either IP or Domain need to be set.')

        return cleaned_data


class PingService(ServicePlugin):
    name = "Ping"
    description = "Check if an IP is pingable."
    config_class = PingPluginConfig
    form_class = PingPluginForm

    def run_check(self, settings):
        log = self.get_logger()

        import subprocess

        host = settings['host']
        timeout = settings['timeout']

        cmd = settings['cmd'] or "ping -c1 -w{timeout} {host}"
        cmd = cmd.format(timeout=timeout, host=host)

        log.debug("Pinging {}".format(host))

        code = subprocess.call(cmd.split(' '))

        if code != 0:
            raise ServiceIsDownException('Could not ping {h} with cmd {cmd}'.format(h=host, cmd=cmd))
