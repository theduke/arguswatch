from celery import Task
from celery.registry import tasks
from celery.utils.log import get_task_logger

from arguswatch.argus_services.models import Service
from arguswatch.argus_services.plugins import ServiceIsDownException, PluginCheckError
from arguswatch.utils.django import get_cls_by_name


class ArgusChecker(Task):
    """
    Run a check plugin.
    """

    name = "arguswatch.checker"

    def __init__(self):
        pass


    def run(self, plugin_cls_name, settings):
        """
        Just load the right plugin class, and then 
        execute the check.

        Return tuple of (RESULT, MSG).
        MSG is empty for UP states.
        """

        plugin = get_cls_by_name(plugin_cls_name)()
        plugin.set_logger(get_task_logger('django'))

        try:
            plugin.run_check(settings)
        except PluginCheckError as e:
            return (Service.CHECK_STATE_KNOWN_ERROR, e.reason)
        except ServiceIsDownException as e:
            return (Service.CHECK_STATE_DOWN, e.info)
        except Exception as e:
            return (Service.CHECK_STATE_UNKNOWN_ERROR, '{}: {}'.format(e.__class__, e))   

        return (Service.CHECK_STATE_UP, '')

tasks.register(ArgusChecker)
