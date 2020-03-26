import abc
from notification.api.serializer import QueuablePushNotificationData

class PushServiceWrapperABC(abc.ABC):
    '''
    Implemented by every Push sender service Wrapper(eg. FCM)
    '''
    @classmethod
    @abc.abstractmethod
    def send(cls, data:QueuablePushNotificationData)->SentResult:
        ...

    @classmethod
    @abc.abstractmethod
    def handle_callback(cls, request_data):
        ...
