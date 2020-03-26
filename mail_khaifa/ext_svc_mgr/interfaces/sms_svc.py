import abc
from notification.serializer import QueuableSmsNotificationData
from .sent_result import SentResult

class SmsServiceWrapperABC(abc.ABC):
    '''
    Implemented by every SMS sender service Wrapper(eg. Twilio, MSG91 etc.)
    '''
    @classmethod
    @abc.abstractmethod
    def send(cls, data:QueuableSmsNotificationData)->SentResult:
        ...

    @classmethod
    @abc.abstractmethod
    def handle_callback(cls, request_data):
        ...