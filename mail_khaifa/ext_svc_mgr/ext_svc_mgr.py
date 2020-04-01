import random, collections, typing
from notification.models import Notification
from notification.interfaces.notification_data import NotificationDataABC
from .interfaces.sms_svc import SmsServiceWrapperABC
from .named_tuples import StateTransition, ExtClientResult

class ExternalServiceManager(object):
    '''
    Class that manages all external service wrappers to send sms, Email, push notifications
    '''
    
    SMS_SENDERS=[]

    @classmethod
    def send(cls, data:NotificationDataABC)->ExtClientResult:
        if data.get_notification_type()==Notification.TYPE_SMS:
            return SMS_SENDERS[random.randint(0, len(SMS_SENDERS))].send(data)

    @classmethod
    def handle_callback(cls, request_data:typing.Dict, client_identifier:str)->StateTransition:
        raise NotImplementedError()
