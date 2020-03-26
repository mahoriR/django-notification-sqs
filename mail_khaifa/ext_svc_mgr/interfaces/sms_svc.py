import abc
from notification.api.serializer import QueuablePushNotificationData

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