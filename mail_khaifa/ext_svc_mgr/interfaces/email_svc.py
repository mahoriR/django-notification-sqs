import abc
from notification.api.serializer import QueuableEmailNotificationData

class EmailServiceWrapperABC(abc.ABC):
    '''
    Implemented by every Email sender service Wrapper(eg. Sendgrid etc.)
    '''
    @classmethod
    @abc.abstractmethod
    def send(cls, data:QueuableEmailNotificationData)->SentResult:
        ...

    @classmethod
    @abc.abstractmethod
    def handle_callback(cls, request_data):
        ...