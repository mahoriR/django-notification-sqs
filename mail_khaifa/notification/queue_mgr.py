import abc, time, enum, typing
from .serializers.serializer import QueuableNotificationDataABC, QueuableNotificationStateABC

from .interfaces.notif_data_writer import NotificationQueueWriterABC
from .interfaces.notif_state_writer import NotificationStateQueueWriterABC

from common_utils.errors import Error

from django.conf import settings
from .tasks import task_enqueue_payload


class QueueWriter(NotificationQueueWriterABC, NotificationStateQueueWriterABC):

    class QueuedEntityType(enum.IntEnum):
        DATA=1
        STATE=2

    '''
       1. Notification Data Queue as priority
       2. Writes to Callback Queue with appropriate delay
    '''
    QUEUE_NAMES={
        QueuableNotificationDataABC.PriorityType.HIGH:settings.HIGH_PRIORITY_QUEUE,
        QueuableNotificationDataABC.PriorityType.MEDIUM:settings.MEDIUM_PRIORITY_QUEUE,
        QueuableNotificationDataABC.PriorityType.LOW:settings.LOW_PRIORITY_QUEUE,
    }

    @classmethod
    def _get_queue_from_priority(cls, priority:int):
        return cls.QUEUE_NAMES[QueuableNotificationDataABC.PriorityType(priority)]

    @classmethod
    def enqueue_notification(cls, data:QueuableNotificationDataABC)->Error.ErrorInfo:
        '''
         Write to CP Queue
        '''
        if data.get_max_timestamp() and (data.get_max_timestamp() < int(time.time())):
            #we need to check, that current Timestamp is not past this.
            return Error.CONSTRAINTS_NOT_POSSIBLE

        queue_data={
            'q_e_type':cls.QueuedEntityType.DATA,
            'payload':data.to_dict()
        }

        task_enqueue_payload.apply_async(
            args=(queue_data,),
            queue=cls._get_queue_from_priority(data.get_priority()))
        return Error.NO_ERROR

    @classmethod
    def enqueue_notification_state_cb(cls, data:QueuableNotificationStateABC)->Error.ErrorInfo:
        queue_data={
            'q_e_type':cls.QueuedEntityType.STATE,
            'payload':data.to_dict()
        }
        task_enqueue_payload.apply_async(
            args=(queue_data,),
            queue=cls._get_queue_from_priority(QueuableNotificationDataABC.PriorityType.LOW))
        return Error.NO_ERROR

    @classmethod
    def get_payload_and_type(cls, data:typing.Dict)->typing.Tuple:
        return data.get('payload'), cls.QueuedEntityType(data.get('q_e_type'))
