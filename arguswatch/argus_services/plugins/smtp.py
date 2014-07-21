from django.db import models
from django.utils.translation import ugettext as _

from django_baseline.forms import CrispyModelForm

from . import ServicePlugin, ServiceIsDownException, PluginCheckError, PluginConfiguratinError
from ..models import ServicePluginConfiguration


class SMTPPluginConfig(ServicePluginConfiguration):
    host = models.CharField(max_length=255, help_text="Server host.")
    port = models.SmallPositiveIntegerField(default=110,
        help_text="Server port. Default is 110 for non SSL, 995 for SSL.")

    METHOD_UNENCRYPTED = 'unencrypted'
    METHOD_STARTTLS = 'starttls'
    METHOD_SSL = 'ssl'
    METHOD_CHOICES = (
        (METHOD_UNENCRYPTED, 'Unencrypted'),
        (METHOD_STARTTLS, 'StartTLS'),
        (METHOD_SSL, 'SSL/TLS'),
    )
    method = models.CharField(max_length=20, choices=METHOD_CHOICES,
        help_text="Connection method")

    check_authentication = models.BooleanField(default=False,
        help_text="Check authentication with specified username and password.")

    AUTH_METHOD_PLAIN = 'plain'
    AUTH_METHOD_CHOICES = (
        ('', ''),
        (AUTH_METHOD_PLAIN, 'PLAIN'),
    )
    auth_method = models.CharField(max_length=50, blank=True,
        choices=AUTH_METHOD_CHOICES, verbose_name="Authentication method")
    username = models.CharField(max_length=255, blank=True, 
        help_text="Username to authenticate with.")
    password = models.CharField(max_length=255, blank=True,
        help_text="Password to authenticate with.")

    timeout = models.SmallPositiveIntegerField(default=30, 
        help_text="Time in seconds the server is allowed to take to respond")

    def get_settings(self):
        return {
            'method': self.method,
            'host': self.host,
            'port': self.port,
            'check_authentication': self.check_authentication,
            'auth_method': self.auth_method,
            'username': self.username,
            'password': self.password,
            'timeout': self.timeout,
        }


    class Meta:
        verbose_name = _('SMTPPluginConfig')
        verbose_name_plural = _('SMTPPluginConfigs')
        app_label = "argus_services"


class SMTPPluginForm(CrispyModelForm):
    class Meta:
        model = SMTPPluginConfig
        fields = [
            'method',
            'host', 'port',
            'check_authentication', 'username', 'password'
        ]


class SMTPService(ServicePlugin):
    name = "SMTP"
    description = "Check an SMTP email server"
    is_passive = False
    config_class = SMTPPluginConfig
    form_class = SMTPPluginForm


    def get_connection(self, settings):
        con = None

        method = settings['method']
        host = settings['host']
        port = settings['port']

        try: 
            if method == SMTPPluginConfig.METHOD_UNENCRYPTED:
                con = smtplib.SMTP(host, port, timeout=timeout)
            elif method == SMTPPluginConfig.METHOD_STARTTLS:
                con = smtplib.SMTP(host, port, timeout=timeout)
                con.starttls()
            elif method == SMTPPluginConfig.METHOD_SSL:
                con = smtplib.SMTP_SSL(host, port, timeout=timeout)
            else:
                raise PluginConfiguratinError("Unknown connection method: " + method)
        except socket.gaierror as e:
            raise ServiceIsDownException("Could not resolve hostname {h}".format(
                host))
        except ssl.SSLError as e:
            raise ServiceIsDownException("SSL error: " + str(e))
        except socket.error as e:
            raise ServiceIsDownException("Socket error: " + str(e))
        except smtplib.SMTPConnectError as e:
            raise ServiceIsDownException("SMTP connect error: " + str(e))

        return con


    def run_check(self, settings):
        log = self.get_logger()

        import SMTPlib
        import socket
        import ssl

        con = self.get_connection(settings)

        if settings['check_authentication']:
            auth_method = settings['auth_method']

            if auth_method == SMTPPluginConfig.AUTH_METHOD_PLAIN:
                try:
                    con.login(settings['username'], settings['password'])
                except smtplib.SMTPHeloError as e:
                    raise ServiceIsDownException("Server HELO error: " + str(e))
                except smtplib.SMTPAuthenticationError as e:
                    raise ServiceIsDownException("Authentication error: " + str(e))
            else:
                raise PluginConfiguratinError('Unknown auth method: ' + auth_method)
