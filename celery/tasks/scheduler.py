import datetime

from celery import Task
from celery.registry import tasks

from arguswatch.argus_services.models import Service


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

        # First, check if a task is registered, and if so, process the task result.
        if service.celery_task_id:
            result  = self.AsyncResult(service.celery_task_id)
            if result.ready():
                self.handle_check_result(service, result)
            else:
                # Task has not finished yet, so just keep on waiting for the 
                # result.
                # TODO: Think about adding a time limit here.
                # TODO: add logging
                return

        # Either no task was running, or the running one was handled properly.
        # So proceed to check if a check needs to be scheduled.
        if service.is_check_needed():
            # Check is needed, so issue it.
            service.issue_check()



    def handle_check_result(self, service, result):
        """
        Handle the result of a check.
        """

        pass

scheduler = ArgusScheduler()