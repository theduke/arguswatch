import datetime
import logging
import time

from django.utils import timezone

from arguswatch.argus_services.models import Service
from arguswatch.celery import checker

class Server:

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger('argus.server')

        # The time a task check is allowed to be completed.
        # If the check task takes longer than that, the check will be 
        # aborted and a new one issued.
        self.check_timeout_threshhold = 600

        # If the main run loop of the server takes less than this amount in
        # seconds, the loop sleeps until the specified time amount is reached
        # to prevent flooding.
        self.run_loop_minimum_time = 30

    def run(self):
        while True:
            start = datetime.datetime.now()
            
            self.check_services()
            
            finish = datetime.datetime.now()
            time_taken = finish - start
            seconds_taken = time_taken.seconds + (time_taken.microseconds / 1000000)

            self.logger.debug("Server loop finished in {} seconds.".format(seconds_taken))

            if seconds_taken < self.run_loop_minimum_time:
                sleep = self.run_loop_minimum_time - time_taken.seconds
                self.logger.debug("Sleeping {} seconds.".format(sleep))
                time.sleep(sleep)

    def check_services(self):
        for service in Service.objects.filter(enabled=True).select_related('config'):
            try:
                self.handle_service(service)
            except Exception as e:
                self.logger.warning("Handling of service {s} failed: {e}".format(
                    s=service, e=e))

    def handle_service(self, service):
        """
        Handle a single service.
        If a task has finished, handle it.

        Then, determine if a check should be scheduled.
        """

        self.logger.debug("Handling Service {} (id: {})".format(service, service.id))

        # First, check if a task is registered, and if so, process the task result.
        if service.celery_task_id:
            result  = checker.AsyncResult(task_id=service.celery_task_id)
            if result.ready():
                self.handle_check_result(service, result)
            else:
                # Task has not finished yet.
                # Check if task is beyond time threshhold. If so, task is discarded and 
                # re-issued. Otherwise, do nothing.

                # TODO: add logging
                if timezone.now() - service.last_issued >= datetime.timedelta(seconds=self.check_timeout_threshhold):
                    # Beyond threshhold, clear task id so task can be re-issued.
                    self.logger.warning("Task id for service {s} has expired. Purging task id: {t}".format(
                        s=service, t=service.celery_task_id))
                    service.celery_task_id = ''
                else:
                    # Nothing to do here...
                    return

        # Either no task was running, or the running one was handled properly.
        # So proceed to check if a check needs to be scheduled.
        if service.is_check_needed():
            self.logger.info('Issuing check for service {}'.format(service))
            # Check is needed, so issue it.
            service.issue_check()


    def handle_check_result(self, service, result):
        """
        Handle the result of a check.
        """

        self.logger.info("Result for service {} is ready. Handling now...".format(service))
        service.handle_check_result(result, log=self.logger)
