import abc
from .queuable_notification_data import QueuableNotificationDataABC
from common_utils.errors import Error

class NotificationQueueWriterABC(abc.ABC):
    '''
       1. Notification Data Queue as priority
    '''

    @classmethod
    @abc.abstractmethod
    def enqueue_notification(cls, priority:int, data:QueuableNotificationDataABC)->Error.ErrorInfo:...

    @classmethod
    @abc.abstractmethod
    def requeue_notification(cls, priority:int, data:QueuableNotificationDataABC)->Error.ErrorInfo:
        '''
        Checks for Queuing timestamp before calling enqueue_notification

        Returns Error if requeuing not valid because time has passed
        '''
        ...
