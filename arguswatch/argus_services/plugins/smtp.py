import smtplib
import socket
import ssl

from django.db import models
from django.utils.translation import ugettext as _
from django import forms

from django_baseline.forms import CrispyModelForm

from . import ServicePlugin, ServiceIsDown, ServiceCheckFailed, PluginConfigurationError
from ..models import ServicePluginConfiguration


class SMTPPluginConfig(ServicePluginConfiguration):
    host = models.CharField(max_length=255, help_text="Server host.")
    port = models.PositiveSmallIntegerField(default=25,
        help_text="Server port. Default is 25 for non SSL, 465 for SSL.")

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
        (AUTH_METHOD_PLAIN, 'PLAIN'),
    )
    auth_method = models.CharField(max_length=50, blank=True,
        choices=AUTH_METHOD_CHOICES, verbose_name="Authentication method")
    username = models.CharField(max_length=255, blank=True, 
        help_text="Username to authenticate with.")
    password = models.CharField(max_length=255, blank=True,
        help_text="Password to authenticate with.")

    timeout = models.PositiveSmallIntegerField(default=30, 
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
            'check_authentication', 'auth_method', 'username', 'password',
        ]


    def clean(self):
        data = super(SMTPPluginForm, self).clean()

        if data['check_authentication'] and not data['auth_method']:
            raise forms.ValidationError("Need to select authentication method if auth check is enabled")
        if data['auth_method'] == SMTPPluginConfig.AUTH_METHOD_PLAIN:
            if not (data['username'] and data['password']):
                raise forms.ValidationError("For PLAIN authentiaction, username and password are required.")

        return data



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
        timeout = settings['timeout']

        try: 
            if method == SMTPPluginConfig.METHOD_UNENCRYPTED:
                con = smtplib.SMTP(host, port, timeout=timeout)
            elif method == SMTPPluginConfig.METHOD_STARTTLS:
                con = smtplib.SMTP(host, port, timeout=timeout)
                con.starttls()
            elif method == SMTPPluginConfig.METHOD_SSL:
                con = smtplib.SMTP_SSL(host, port, timeout=timeout)
            else:
                raise PluginConfigurationError("Unknown connection method: " + method)
        except socket.gaierror as e:
            raise ServiceIsDown("Could not resolve hostname {h}".format(
                host))
        except ssl.SSLError as e:
            raise ServiceIsDown("SSL error: " + str(e))
        except socket.error as e:
            raise ServiceIsDown("Socket error: " + str(e))
        except smtplib.SMTPConnectError as e:
            raise ServiceIsDown("SMTP connect error: " + str(e))

        return con


    def run_check(self, settings):
        log = self.get_logger()

        con = self.get_connection(settings)

        if settings['check_authentication']:
            auth_method = settings['auth_method']

            if auth_method == SMTPPluginConfig.AUTH_METHOD_PLAIN:
                try:
                    con.login(settings['username'], settings['password'])
                except smtplib.SMTPHeloError as e:
                    raise ServiceIsDown("Server HELO error: " + str(e))
                except smtplib.SMTPAuthenticationError as e:
                    con.quit()
                    raise ServiceIsDown("Authentication error: " + str(e))
            else:
                raise PluginConfigurationError('Unknown auth method: ' + auth_method)

        con.quit()
