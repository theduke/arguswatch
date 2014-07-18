import datetime

from django.utils import timezone

from celery import Task
from celery.registry import tasks
from celery.utils.log import get_task_logger

from arguswatch.argus_services.models import Service

from .checker import ArgusChecker

log = get_task_logger('django')


class ArgusScheduler(Task):
    """
    Scheduler.
    This task will be run constantly, and will handle finished checker tasks,
    as well as issuing new checks when time limits are reached.
    """


    def __init__(self):
        pass

    def run(self):
        for service in Service.objects.filter(enabled=True).select_related('service_config'):
            self.handle_service(service)

    def handle_service(self, service):
        """
        Handle a single service.
        If a task has finished, handle it.

        Then, determine if a check should be scheduled.
        """

        log.debug("Handling Service {} (id: {})".format(service, service.id))

        # First, check if a task is registered, and if so, process the task result.
        if service.celery_task_id:
            result  = self.AsyncResult(service.celery_task_id)
            if result.ready():
                self.handle_check_result(service, result)
            else:
                # Task has not finished yet.
                # Check if task is beyond time threshhold. If so, task is discarded and 
                # re-issued. Otherwise, do nothing.

                # TODO: add logging

                if timezone.now() - service.last_issued >= datetime.timedelta(seconds=600):
                    # Beyond threshhold, clear task id so task can be re-issued.
                    service.celery_task_id = ''
                else:
                    # Nothing to do here...
                    return


        # Either no task was running, or the running one was handled properly.
        # So proceed to check if a check needs to be scheduled.
        if service.is_check_needed():
            log.info('Issuing check for service {}'.format(service))
            # Check is needed, so issue it.
            service.issue_check()


    def handle_check_result(self, service, result):
        """
        Handle the result of a check.
        """

        log.info("Result for service {} is ready. Handling now...".format(service))

        state, msg = result.get()

        # Event to trigger.
        evt = None

        if state == Service.CHECK_STATE_UP or state == Service.CHECK_STATE_DOWN:
            evt = service.determine_event(state)
            log.debug("Determined evt for service {}: {}".format(service, evt))

            service.trigger_event(evt)
            service.last_checked = timezone.now()

            service.celery_task_id = ''
            service.save()

            notifications = service.determine_notifications_to_send(evt)

            for n in notifications:
                log.debug("Sending notification {} for service {}".format(n, service))
                n. do_notify(service, evt)

        elif state == Service.CHECK_STATE_KNOWN_ERROR:
            log.warning("Service {} (plugin: {}: KNOWN_ERROR: {m}".format(
                service, service.plugin, msg
            ))
            # TODO: handle with retry.
        elif state == Service.CHECK_STATE_UNKNOWN_ERROR:
            # TODO: handle with retry.
            log.warning("Service {} (plugin: {}: UNKNOWN_ERROR: {}".format(
                service, service.plugin, msg
            ))

tasks.register(ArgusScheduler)
