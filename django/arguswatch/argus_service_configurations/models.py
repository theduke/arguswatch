from django.db import models


class ServiceConfiguration(models.Model):
    """
    Model for holding service configuration regarding
    check intervals, max retry counts, notifications, etc.
    
    This is in an extra model to allow this settings to be used as templates.
    """

    # Specifies, if this configuration is a template.
    # False if a service configurtion is customized.
    is_template = models.BooleanField()

    # Will be blank for custom service configs.
    name = models.CharField(max_length=50, blank=True, unique=True, verbose_name='Descriptive name for this service configuration template.')

    check_interval = models.PositiveIntegerField(verbose_name="Interval in which checks for this service are run if state is OK.")
    retry_interval_soft = models.PositiveIntegerField(verbose_name='Interval in which checks for this service are run if service is DOWN state type is SOFT.')
    retry_interval_hard = models.PositiveIntegerField(verbose_name='Time after which a retry is run if service is DOWN and state type is HARD')
    max_retries_soft = models.PositiveSmallIntegerField(verbose_name='How many retries are run for a service that goes DOWN.')


    class Meta:
        verbose_name = _('ServiceConfiguration')
        verbose_name_plural = _('ServiceConfigurations')
