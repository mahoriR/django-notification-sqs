import abc
from notification.serializers.serializer import QueuableSmsNotificationData
from .sent_result import SentResultABC

class SmsServiceWrapperABC(abc.ABC):
    '''
    Implemented by every SMS sender service Wrapper(eg. Twilio, MSG91 etc.)
    '''
    @classmethod
    @abc.abstractmethod
    def send(cls, data:QueuableSmsNotificationData)->SentResultABC:
        ...

    @classmethod
    @abc.abstractmethod
    def handle_callback(cls, request_data):
        ...