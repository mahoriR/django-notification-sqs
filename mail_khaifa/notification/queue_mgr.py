import abc, time, enum, typing
from .serializers.serializer import QueuableNotificationDataABC, QueuableNotificationStateABC

from .interfaces.notif_data_writer import NotificationQueueWriterABC
from .interfaces.notif_state_writer import NotificationStateQueueWriterABC

from common_utils.errors import Error

class QueueWriter(NotificationQueueWriterABC, NotificationStateQueueWriterABC):

    class QueuedEntityType(enum.IntEnum):
        DATA=1
        STATE=2

    '''
       1. Notification Data Queue as priority
       2. Writes to Callback Queue with appropriate delay
    '''
    P1_QUEUE_NUM=0
    P2_QUEUE_NUM=0
    P3_QUEUE_NUM=0
    P3_MAX_QUEUES=4
    P2_MAX_QUEUES=3
    P1_MAX_QUEUES=2

    # When using Multiple instances of service, add prefix to these queue names
    # and ask CP_Queue to create if does not exists
    QUEUE_NAMES={
        3:['NAME_3', 'NAME_2', 'NAME_1', 'NAME_0'],
        2:['NAME_2', 'NAME_1', 'NAME_0'],
        1:['NAME_1', 'NAME_0'],
    }
    QUEUES=[]
    QUEUE_CONFIG={
        3:(P3_QUEUE_NUM, P3_MAX_QUEUES),
        2:(P2_QUEUE_NUM, P2_MAX_QUEUES),
        1:(P1_QUEUE_NUM, P1_MAX_QUEUES),
    }

    @classmethod
    def _get_queue_from_priority(cls, priority:int):
        '''
        Returns queue name/URL for priority.
        Balances against available Queues
        '''
        q_config=QUEUE_CONFIG[priority]
        q_num=(q_config[0]+1)%q_config
        QUEUE_CONFIG[priority]=(q_num, q_config[1])
        return QUEUE_NAMES[priority][q_num]

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

        #if we are pushing to external Queue, we need to add our CB and other params as well.
        return Error.NO_ERROR

    @classmethod
    def enqueue_notification_state_cb(cls, data:QueuableNotificationStateABC)->Error.ErrorInfo:
        queue_data={
            'q_e_type':cls.QueuedEntityType.STATE,
            'payload':data.to_dict()
        }
        return Error.NO_ERROR

    @classmethod
    def get_payload_and_type(cls, data:typing.Dict)->typing.Dict:
        return data.get('payload'), cls.QueuedEntityType(data.get('q_e_type'))
