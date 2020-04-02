import uuid
import json

from django.core.exceptions import MultipleObjectsReturned

from celery.exceptions import SoftTimeLimitExceeded
from celery.decorators import task
from celery.utils.log import get_task_logger

from .ext_svc_interfacer import ExternalSvcInterfacer

logger = get_task_logger(__name__)

@task(
    name="task_enqueue_payload",
    queue="LOW_PRIORITY",
    bind=True,
    max_retries=3,
    soft_time_limit=10)
def task_enqueue_payload(self, task_payload):
    try:
        ExternalSvcInterfacer.get_instance(None).handle_enqued_notification_payload(task_payload)
    except SoftTimeLimitExceeded as e:
        raise self.retry(countdown=3 ** self.request.retries, exc=e)
    except Exception as e:
        logger.error("{0}-{1}-{2}".format(__name__, "task_enqueue_payload", str(e)))
        raise self.retry(countdown=3 ** self.request.retries, exc=e)
