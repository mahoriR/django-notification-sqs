import abc, typing
from notification.api.serializer import QueuablePushNotificationData
from ..named_tuples import StateTransition, ExtClientResult

class PushServiceWrapperABC(abc.ABC):
    '''
    Implemented by every Push sender service Wrapper(eg. FCM)
    '''
    @classmethod
    @abc.abstractmethod
    def send(cls, data:QueuablePushNotificationData)->ExtClientResult:
        ...

    @classmethod
    @abc.abstractmethod
    def handle_callback(cls, request_data:typing.Dict)->StateTransition:
        ...
