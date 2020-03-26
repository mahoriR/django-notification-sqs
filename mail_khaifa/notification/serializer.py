import abc, uuid, collections
import typing

from mail_khaifa.cp_utils.errors import ErrorInfo, CpError

from mail_khaifa.cp_utils.interfaces.request_serializer import RequestABC

from .models import AddrEntity, Notification

from .interfaces.queuable_notification_data import QueuableNotificationDataABC
from .interfaces.queuable_notification_state import QueuableNotificationStateABC
from .interfaces.addressable_entity import AddressableEntityABC


class QueuableNotificationData(QueuableNotificationDataABC):
    def __init__(self, to_entity:list, to_entity_grp:list, to_entity_type:int, addressing_type:str,
                    cb_url:str, cb_states:list):
        pass
    
    def to_json(self):
        return super().to_json()
    
    def from_json(self):
        return super().from_json()
    
    def get_notification_type(self):
        return super().get_notification_type()

class QueuableSmsNotificationData(QueuableNotificationData, RequestABC):
    class SmsType(object):
        __slots__=[]
        TRANSACTIONAL   = 3
        PROMOTIONAL     = 2
        OTP             = 1

    def __init__(self, n_id:str, from_phone:str, from_code:str,
                    sms_content:str, sms_type:int,
                    to_entity:list, to_entity_grp:list, to_entity_type:int, addressing_type:str,
                    cb_url:str, cb_states:list):
        '''
        *Returns SMS Queue Data*

        nid - Notification ID. Pass None if notification service shall generate
        from_phone - Phone number to use for sending this SMS (Used for promotional SMS only)

        from_code - SMS Code to use for sending this SMS (Used for Transactional/OTP SMS only)

        sms_content - SMS Text (Max 512 Chars)
        
        sms_type - Type of SMS. Possible values -
                        
                        1. TRANSACTIONAL   = 3
                        2. PROMOTIONAL     = 2
                        3. OTP             = 1

        to_entity -  List of entity IDs to send this SMS

        to_entity_grp - List of entity Groups IDs to sent this SMS. If List is empty no filtering on groups is done.

        to_entity_type - Used along with to_entity_grp. Possible values in

                        1. TYPE_CUSTOMER = 1
                        2. TYPE_DELIVERY_AGENT = 2
                        3. TYPE_MERCHANT = 3

        addressing_type - Used to decide if to_entity is used or to_entity_grp. Possible values in -

                        1. ENTITY = 'entity'
                        2. ENTITY_GROUP = 'entity_grp'

        priority - What is priority of this message. Possible values include -
                        
                        1. HIGH = 3 #highest
                        2. MEDIUM = 2
                        3. LOW = 1 #lowest

        cb_url - Call back URL. Will be called for state transition updates. Can be None
        cb_states - List of possible states. Cb will be called when transitioning to these states.
                        
                        1. STATE_QUEUED = 1
                        2. STATE_SENT = 2
                        3. STATE_DELIVERED = 3
                        4. STATE_READ = 4
                        5. STATE_FAILED = 5

        '''
        super().__init__(to_entity, to_entity_grp, to_entity_type, addressing_type, cb_url, cb_states)
        pass

    @classmethod
    def from_request(cls, request_data)->(QueuableSmsNotificationData, ErrorInfo):
        if request_data.get('addressing_type', None) == cls.AddressingType.ENTITY:
            if request_data.get('nid', None) is None:
                request_data['nid']=uuid.uuid4()
            return cls(request_data), CpError.NO_ERROR
        elif request_data.get('addressing_type', None) == cls.AddressingType.ENTITY_GROUP:
            sms_queue_data_list=[]
            for eid in request_data.get('to_entity', []):
                sms_queue_data_list.append(cls(request_data))
            return sms_queue_data_list, CpError.NO_ERROR
        else:
            raise NotImplementedError()

class QueuableEmailNotificationData(QueuableNotificationData, RequestABC):
    '''
        *Returns Email Queue Data*

        nid - Notification ID. Pass None if notification service shall generate
        from_email - Email to use for sending this Email

        email_subject - Subject Text 
        email_body - Body Text

        to_entity -  List of entity IDs to send this SMS

        to_entity_grp - List of entity Groups IDs to sent this SMS. If List is empty no filtering on groups is done.

        to_entity_type - Used along with to_entity_grp. Possible values in

                        1. TYPE_CUSTOMER = 1
                        2. TYPE_DELIVERY_AGENT = 2
                        3. TYPE_MERCHANT = 3

        addressing_type - Used to decide if to_entity is used or to_entity_grp. Possible values in -

                        1. ENTITY = 'entity'
                        2. ENTITY_GROUP = 'entity_grp'

        priority - What is priority of this message. Possible values include -
                        
                        1. HIGH = 3 #highest
                        2. MEDIUM = 2
                        3. LOW = 1 #lowest

        cb_url - Call back URL. Will be called for state transition updates. Can be None
        cb_states - List of possible states. Cb will be called when transitioning to these states.
                        
                        1. STATE_QUEUED = 1
                        2. STATE_SENT = 2
                        3. STATE_DELIVERED = 3
                        4. STATE_READ = 4
                        5. STATE_FAILED = 5

        '''

class QueuablePushNotificationData(QueuableNotificationData, RequestABC):
    '''
        *Returns iOS/Android Push Queue Data*

        push_title - Push Notification Title
        push_body - Push Notification body
        push_data - Push Notification data(dict)

        to_entity -  List of entity IDs to send this SMS

        to_entity_grp - List of entity Groups IDs to sent this SMS. If List is empty no filtering on groups is done.

        to_entity_type - Used along with to_entity_grp. Possible values in

                        1. TYPE_CUSTOMER = 1
                        2. TYPE_DELIVERY_AGENT = 2
                        3. TYPE_MERCHANT = 3

        addressing_type - Used to decide if to_entity is used or to_entity_grp. Possible values in -

                        1. ENTITY = 'entity'
                        2. ENTITY_GROUP = 'entity_grp'

        priority - What is priority of this message. Possible values include -
                        
                        1. HIGH = 3 #highest
                        2. MEDIUM = 2
                        3. LOW = 1 #lowest

        cb_url - Call back URL. Will be called for state transition updates. Can be None
        cb_states - List of possible states. Cb will be called when transitioning to these states.
                        
                        1. STATE_QUEUED = 1
                        2. STATE_SENT = 2
                        3. STATE_DELIVERED = 3
                        4. STATE_READ = 4
                        5. STATE_FAILED = 5

        '''

class QueuableNotificationState(QueuableNotificationStateABC):
    pass

class AddressableEntity(AddressableEntityABC, RequestABC):
    def __init__(self, eid:uuid, e_type:int, phones:list, emails:list, fcm_tokens:list):
        raise NotImplemented()
    @classmethod
    def from_request(cls, request_data)->(AddressableEntity, ErrorInfo):
        if request_data and                                     \
        ('eid' in request_data) and                             \
        ('e_type' in request_data) and                          \
        ('e_type' in zip(AddrEntity.ENTITY_TYPE_CHOICES)[0]):
            return cls(
                request_data.get('eid'), request_data.get('e_type'),
                request_data.get('phones', list()),
                request_data.get('emails', list()),
                request_data.get('fcm_tokens', list())
                )
        return CpError.INVALID_PARAMETERS
