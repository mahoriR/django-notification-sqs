import abc
from .queuable_notification_state import QueuableNotificationStateABC
from cp_utils.errors import ErrorInfo

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
