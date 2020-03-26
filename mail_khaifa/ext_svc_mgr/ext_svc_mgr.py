import random
from notification.api.serializer import NotificationDataABC
from notification.models import Notification
from .interfaces import SmsServiceWrapperABC

class MSG91Wrapper(SmsServiceWrapperABC):
    '''
    Send SMS using MSG91
    '''
    @classmethod
    def send(cls, data):
        raise NotImplementedError()
    @classmethod
    def handle_callback(cls, request_data):
        raise NotImplementedError()

class ExternalServiceManager(object):
    '''
    Class that manages all external service wrappers to send sms, Email, push notifications
    '''
    SMS_SENDERS=[MSG91Wrapper]

    @classmethod
    def send(cls, data:NotificationDataABC)->SentResult:
        if data.get_notification_type()==Notification.TYPE_SMS:
            return SMS_SENDERS[random.randint(0, len(SMS_SENDERS))].send(data)

    @classmethod
    def handle_callback(cls, request_data):
        raise NotImplementedError()
