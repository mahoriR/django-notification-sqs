import abc
from .queuable_notification_state import QueuableNotificationStateABC
from common_utils.errors import Error

class NotificationStateQueueWriterABC(abc.ABC):
    '''
    1. Writes to Callback Queue with appropriate delay
    '''
    @classmethod
    @abc.abstractmethod
    def enqueue_notification_state_cb(cls, data:QueuableNotificationStateABC)->Error.ErrorInfo:...
