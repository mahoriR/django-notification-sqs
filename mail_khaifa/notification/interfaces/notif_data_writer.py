import abc
from .queuable_notification_data import QueuableNotificationDataABC
from common_utils.errors import Error

class NotificationQueueWriterABC(abc.ABC):
    '''
       1. Notification Data Queue as priority
    '''

    @classmethod
    @abc.abstractmethod
    def enqueue_notification(cls, data:QueuableNotificationDataABC)->Error.ErrorInfo:...
