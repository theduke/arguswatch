from celery import Task
from celery.registry import tasks

from arguswatch.argus_services.models import Service
from arguswatch.argus_services.plugins import ServiceIsDownException, PluginCheckError
from arguswatch.utils.django import get_cls_by_name


class ArgusChecker(Task):
    """
    Run a check plugin.
    """

    STATE_UP = "up"
    STATE_DOWN = "down"
    STATE_KNOWN_ERROR = "known_error"
    STATE_UNKNOWN_ERROR = "unknown_error"


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

        try:
            plugin.run_check(settings)
        except PluginCheckError as e:
            return (self.STATE_KNOWN_ERROR, e.reason)
        except ServiceIsDownException as e:
            return (self.STATE_DOWN, e.info)
        except Exception as e:
            return (self.STATE_UNKNOWN_ERROR, '{}: {}'.format(e.__class__, e))   

        return (self.STATE_UP, '')

tasks.register(ArgusChecker)
checker = ArgusChecker()
