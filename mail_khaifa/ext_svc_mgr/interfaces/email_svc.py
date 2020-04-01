import abc, typing
from notification.api.serializer import QueuableEmailNotificationData
from ..named_tuples import StateTransition, ExtClientResult

class EmailServiceWrapperABC(abc.ABC):
    '''
    Implemented by every Email sender service Wrapper(eg. Sendgrid etc.)
    '''
    @classmethod
    @abc.abstractmethod
    def send(cls, data:QueuableEmailNotificationData)->ExtClientResult:
        ...

    @classmethod
    @abc.abstractmethod
    def handle_callback(cls, request_data:typing.Dict)->StateTransition:
        ...