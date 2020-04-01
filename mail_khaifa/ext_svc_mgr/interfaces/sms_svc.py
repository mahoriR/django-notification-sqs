import abc, typing
from notification.serializers.serializer import QueuableSmsNotificationData
from ..named_tuples import StateTransition, ExtClientResult

class SmsServiceWrapperABC(abc.ABC):
    '''
    Implemented by every SMS sender service Wrapper(eg. Twilio, MSG91 etc.)
    '''
    @classmethod
    @abc.abstractmethod
    def send(cls, data:QueuableSmsNotificationData)->ExtClientResult:
        ...

    @classmethod
    @abc.abstractmethod
    def handle_callback(cls, request_data:typing.Dict)->StateTransition:
        ...