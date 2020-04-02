import uuid
import json

from django.core.exceptions import MultipleObjectsReturned

from celery.exceptions import SoftTimeLimitExceeded
from celery.decorators import task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@task(
    name="task_handle_high_priority",
    queue="HIGH_PRIORITY",
    bind=True,
    max_retries=2,
    soft_time_limit=10)
def task_handle_high_priority(self, task_payload):
    try:
        pass
    except SoftTimeLimitExceeded as e:
        raise self.retry(countdown=3 ** self.request.retries, exc=e)
    except Exception as e:
        logger.error("{0}-{1}-{2}".format(__name__, "task_handle_high_priority", str(e)))
        raise self.retry(countdown=3 ** self.request.retries, exc=e)


@task(
    name="task_handle_medium_priority",
    queue="MEDIUM_PRIORITY",
    bind=True,
    max_retries=2,
    soft_time_limit=10)
def task_handle_medium_priority(self, task_payload):
    try:
        pass
    except SoftTimeLimitExceeded as e:
        raise self.retry(countdown=3 ** self.request.retries, exc=e)
    except Exception as e:
        logger.error("{0}-{1}-{2}".format(__name__, "task_handle_high_priority", str(e)))
        raise self.retry(countdown=3 ** self.request.retries, exc=e)


@task(
    name="task_handle_low_priority",
    queue="LOW_PRIORITY",
    bind=True,
    max_retries=2,
    soft_time_limit=10)
def task_handle_low_priority(self, task_payload):
    try:
        pass
    except SoftTimeLimitExceeded as e:
        raise self.retry(countdown=3 ** self.request.retries, exc=e)
    except Exception as e:
        logger.error("{0}-{1}-{2}".format(__name__, "task_handle_high_priority", str(e)))
        raise self.retry(countdown=3 ** self.request.retries, exc=e)
