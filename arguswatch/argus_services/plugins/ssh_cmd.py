from django.db import models
from django.utils.translation import ugettext as _

from django_baseline.forms import CrispyModelForm

from ..models import ServicePluginConfiguration

from . import ServicePlugin, ServiceIsDown, PluginCheckError, PluginConfigurationError
from .ssh import SSHPluginConfig, SSHService


class SSHCmdPluginConfig(SSHPluginConfig):
    command = models.TextField(help_text="The command to execute on the server.")

    def get_settings(self):
        settings = super(SSHCmdPluginConfig, self).get_settings()
        settings['command'] = self.command
        return settings

    class Meta:
        verbose_name = _('SSHCmdPluginConfig')
        verbose_name_plural = _('SSHCmdPluginConfigs')
        app_label = "argus_services"
 


class SSHCmdPluginForm(CrispyModelForm):
    class Meta:
        model = SSHCmdPluginConfig
        fields = [
            'host', 'port',
            'auth_method', 'username', 'password', 'private_key',
            'timeout',
        ]


class SSHCmdService(SSHService):
    name = "SSHCmd"
    description = "Check an SSHCmd server"
    is_passive = False
    config_class = SSHCmdPluginConfig
    form_class = SSHCmdPluginForm

    def run_check(self, settings):
        log = self.get_logger()
        client = self.get_client(settings)

        stdin, stdout, stderr = client.exec_command(settings['command'])
        print(stdout.channel.recv_exit_status())
