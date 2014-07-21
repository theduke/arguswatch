from django.db import models
from django.utils.translation import ugettext as _

from django_baseline.forms import CrispyModelForm

from . import ServicePlugin, ServiceIsDownException, PluginCheckError, PluginConfiguratinError
from ..models import ServicePluginConfiguration


class SSHPluginConfig(ServicePluginConfiguration):
    host = models.CharField(max_length=255, help_text="Server host.")
    port = models.SmallPositiveIntegerField(default=22,
        help_text="Server port. Default is 22.")

    AUTH_METHOD_PASSWORD = 'password'
    AUTH_METHOD_PRIVATE_KEY = 'key'
    AUTH_METHOD_CHOICES = (
        (AUTH_METHOD_PASSWORD, 'Password'),
        (AUTH_METHOD_PRIVATE_KEY, 'Private Key'),
    )
    auth_method = models.CharField(max_length=50, blank=True,
        choices=AUTH_METHOD_CHOICES, verbose_name="Authentication method.")

    username = models.CharField(max_length=255, blank=True, 
        help_text="Username to authenticate with.")
    password = models.CharField(max_length=255, blank=True,
        help_text="Password to authenticate with.")
    private_key = models.TextField(blank=True)

    timeout = models.SmallPositiveIntegerField(default=30, 
        help_text="Time in seconds the server is allowed to take to respond")

    def get_settings(self):
        return {
            'host': self.host,
            'port': self.port,
            'auth_method': self.auth_method,
            'username': self.username,
            'password': self.password,
            'private_key': self.private_key,
            'timeout': self.timeout,
        }


    class Meta:
        verbose_name = _('SSHPluginConfig')
        verbose_name_plural = _('SSHPluginConfigs')
        app_label = "argus_services"
 


class SSHPluginForm(CrispyModelForm):
    class Meta:
        model = SSHPluginConfig
        fields = [
            'host', 'port',
            'auth_method', 'username', 'password', 'private_key',
            'timeout',
        ]


class SSHService(ServicePlugin):
    name = "SSH"
    description = "Check an SSH server"
    is_passive = False
    config_class = SSHPluginConfig
    form_class = SSHPluginForm

    def get_client(self, settings):
        from paramiko import client
        from paramiko import ssh_exception

        c = client.SSHClient()
        # Make host key acceptance optional.
        c.set_missing_host_key_policy(client.WarningPolicy())

        host = settings['host']
        port = settings['port']
        method = settings['auth_method']

        args = {'port': port}
        if method == SSHPluginConfig.AUTH_METHOD_PASSWORD:
            args['username'] = settings['username']
            args['password'] = settings['password']
        elif method == SSHPluginConfig.AUTH_METHOD_PRIVATE_KEY:
            args['pkey'] = settings['private_key']
        else:
            raise PluginConfiguratinError("Unknown authentication method: " + method)

        try:
            c.connect(host, **args)
        except ssh_exception.AuthenticationException as e:
            raise ServiceIsDownException("Authentication failed: " + str(e))
        except ssh_exception.BadAuthenticationType as e:
            raise ServiceIsDownException("Unsupported authentication type: " + str(e))
        except ssh_exception.ChannelException as e:
            raise ServiceIsDownException("SSH channel open failed: " + str(e))
        except ssh_exception.SSHException as e:
            raise ServiceIsDownException("SSH error: " + str(e))

        return c

    def run_check(self, settings):
        log = self.get_logger()
        con = self.get_client(settings)
