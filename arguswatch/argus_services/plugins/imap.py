import imaplib
import socket
import ssl

from django.db import models
from django.utils.translation import ugettext as _
from django import forms

from django_baseline.forms import CrispyModelForm

from . import ServicePlugin, PluginConfigurationError, ServiceIsDown, ServiceHasWarning, ServiceCheckFailed
from ..models import ServicePluginConfiguration


class IMAPPluginConfig(ServicePluginConfiguration):
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

    host = models.CharField(max_length=255, help_text="Server host.")
    port = models.PositiveSmallIntegerField(default=143,
        help_text="Server port. Default is 143 for non SSL, 993 for SSL.")

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

    def get_settings(self):
        return {
            'method': self.method,
            'host': self.host,
            'port': self.port,
            'check_authentication': self.check_authentication,
            'auth_method': self.auth_method,
            'username': self.username,
            'password': self.password
        }


    class Meta:
        verbose_name = _('IMAPPluginConfig')
        verbose_name_plural = _('IMAPPluginConfigs')
        app_label = "argus_services"
 


class IMAPPluginForm(CrispyModelForm):
    class Meta:
        model = IMAPPluginConfig
        fields = [
            'method',
            'host', 'port',
            'check_authentication', 'auth_method', 'username', 'password'
        ]

    def clean(self):
        data = super(IMAPPluginForm, self).clean()

        if data['check_authentication'] and not data['auth_method']:
            raise forms.ValidationError("Need to select authentication method if auth check is enabled")
        if data['auth_method'] == IMAPPluginConfig.AUTH_METHOD_PLAIN:
            if not (data['username'] and data['password']):
                raise forms.ValidationError("For PLAIN authentiaction, username and password are required.")

        return data


class IMAPService(ServicePlugin):
    name = "IMAP"
    description = "Check an IMAP email server"
    is_passive = False
    config_class = IMAPPluginConfig
    form_class = IMAPPluginForm

    def get_connection(self, settings):
        con = None

        method = settings['method']
        host = settings['host']
        port = settings['port']

        try: 
            if method == IMAPPluginConfig.METHOD_UNENCRYPTED:
                con = imaplib.IMAP4(host, port)
            elif method == IMAPPluginConfig.METHOD_STARTTLS:
                con = imaplib.IMAP4(host, port)
                con.starttls()
            elif method == IMAPPluginConfig.METHOD_SSL:
                con = imaplib.IMAP4_SSL(host, port)
            else:
                raise PluginConfigurationError("Unknown connection method: " + method)
        except socket.gaierror as e:
            raise ServiceIsDown("Could not resolve hostname {h}".format(
                host))
        except ssl.SSLError as e:
            raise ServiceIsDown("SSL error: " + str(e))
        except socket.error as e:
            raise ServiceIsDown("Socket error: " + str(e))
        except imaplib.IMAP4.abort as e:
            raise ServiceIsDown("IMAP error: " + str(e))

        return con

    def run_check(self, settings):
        log = self.get_logger()

        con = self.get_connection(settings)
        
        # Handle authentication.
        if settings['check_authentication']:
            auth_method = settings['auth_method']

            if auth_method == IMAPPluginConfig.AUTH_METHOD_PLAIN:
                try:
                    con.login(settings['username'], settings['password'])
                except imaplib.IMAP4.error as e:
                    con.logout()
                    raise ServiceIsDown("Authentication failed: " + str(e))
            else:
                raise PluginConfigurationError('Unknown auth method: ' + auth_method)


        con.logout()