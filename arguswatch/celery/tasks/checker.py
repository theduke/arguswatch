from celery import Task
from celery.registry import tasks
from celery.utils.log import get_task_logger

from arguswatch.argus_services.models import Service
from arguswatch.argus_services.plugins import PluginImplementationError, PluginConfigurationError, ServiceCheckFailed, ServiceIsDown, ServiceHasWarning
from arguswatch.utils.django import get_cls_by_name


class ArgusChecker(Task):
    """
    Run a check plugin.
    """

    name = "arguswatch.checker"

    def __init__(self):
        pass


    def run(self, plugin_cls_name, settings, logger=None):
        """
        Just load the right plugin class, and then 
        execute the check.

        Return tuple of (RESULT, MSG).
        MSG is empty for UP states.
        """

        plugin = get_cls_by_name(plugin_cls_name)()
        plugin.set_logger(logger or get_task_logger('django'))

        msg = None
        try:
            msg = plugin.run_check(settings)
        except PluginImplementationError as e:
            return (Service.STATE_UNKNOWN, e.message)
        except PluginConfigurationError as e:
            return (Service.STATE_UNKNOWN, "Plugin {} is misconfigured: {}".format(
                plugin_cls_name, e.message))
        except ServiceCheckFailed as e:
            return (Service.STATE_UNKNOWN, "Service check failed: " + e.reason)
        except ServiceIsDown as e:
            return (Service.STATE_DOWN, e.message)
        except ServiceHasWarning as e:
            return (Service.STATE_WARNING, e.message)
        except Exception as e:
            return (Service.STATE_UNKNOWN, 'Unknown exception: {}: {}'.format(
                e.__class__, e))   

        return (Service.STATE_OK, msg or '')

tasks.register(ArgusChecker)
