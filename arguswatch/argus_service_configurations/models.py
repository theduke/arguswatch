from django.db import models
from django.utils.translation import ugettext as _


class ServiceConfiguration(models.Model):
    """
    Model for holding service configuration regarding
    check intervals, max retry counts, notifications, etc.
    
    This is in an extra model to allow this settings to be used as templates.
    """

    # Specifies, if this configuration is a template.
    # False if a service configurtion is customized.
    is_template = models.BooleanField(default=True)

    # Will be blank for custom service configs.
    name = models.CharField(max_length=50, blank=True, unique=True, help_text='Descriptive name for this service configuration template.')
    description = models.TextField(blank=True)

    check_interval_ok = models.PositiveIntegerField(default=60*15, 
        help_text="Check interval if service is OK in seconds.")
    check_interval_provisional = models.PositiveIntegerField(default=60*5, 
        help_text='Check interval for provisional states (down, unknown) in seconds.')
    check_interval_warning = models.PositiveIntegerField(default=60*10, 
        help_text='Check interval if service state is WARNING in seconds.')
    check_interval_down = models.PositiveIntegerField(default=5*10, 
        help_text='Check interval if service is DOWN in seconds.')
    check_interval_unknown = models.PositiveIntegerField(default=5*10, 
        help_text='Check interval if service is UNKNOWN in seconds.')
    max_retries = models.PositiveSmallIntegerField(default=3, 
        help_text='Number of retries before a provisional state is locked in (applies to down and unknown)')

    passive_check_allowed = models.BooleanField(default=False)
    passive_check_ips = models.TextField(blank=True, help_text='Optional list of IPs that are allowed to deliver passive checks. Separated by ;')
    passive_check_api_key = models.CharField(max_length=100, blank=True, help_text='API key that a passive check sender must include in the request. Options: GET parameter ?api-key=KEY. Http basic auth, api-key as username, password is ignored.')

    api_can_trigger_events = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('ServiceConfiguration')
        verbose_name_plural = _('ServiceConfigurations')

    def __str__(self):
        return self.name

    def get_passive_check_ips(self):
        """
        Return the ips that are allowed to provide a passive check.
        Returns None if all IPs are allowed to.
        """

        return self.passive_check_ips.split(";") if self.passive_check_ips else None
