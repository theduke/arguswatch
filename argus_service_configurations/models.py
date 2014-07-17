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

    check_interval = models.PositiveIntegerField(default=60*10, help_text="Interval in which checks for this service are run if state is OK.")
    retry_interval_soft = models.PositiveIntegerField(default=60*2, help_text='Interval in which checks for this service are run if service is DOWN state type is SOFT.')
    retry_interval_hard = models.PositiveIntegerField(default=60*10, help_text='Time after which a retry is run if service is DOWN and state type is HARD')
    max_retries_soft = models.PositiveSmallIntegerField(default=3, help_text='How many retries are run for a service that goes DOWN.')


    class Meta:
        verbose_name = _('ServiceConfiguration')
        verbose_name_plural = _('ServiceConfigurations')


    def __str__(self):
        return self.name
