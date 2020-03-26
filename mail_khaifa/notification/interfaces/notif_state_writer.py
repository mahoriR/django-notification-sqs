import abc
from .api.serializer import QueuableNotificationStateABC
from mail_khaifa.cp_utils.error import ErrorInfo

class NotificationStateQueueWriterABC(abc.ABC):
    '''
    1. Writes to Callback Queue with appropriate delay
    '''
    @classmethod
    @abc.abstractmethod
    def enqueue_notification_state_cb(cls, data:QueuableNotificationStateABC)->ErrorInfo:...

    @classmethod
    @abc.abstractmethod
    def enqueue_notification_state_cb(cls, data:QueuableNotificationStateABC)->ErrorInfo:...
