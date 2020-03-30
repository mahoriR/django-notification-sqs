import abc, uuid, collections, enum
from typing import List

from common_utils.errors import Error
from common_utils.exceptions import IllegalArgumentError

from common_utils.interfaces.request_serializer import RequestABC

from ..models import AddrEntity, Notification

from ..interfaces.queuable_notification_data import QueuableNotificationDataABC
from ..interfaces.queuable_notification_state import QueuableNotificationStateABC
from ..interfaces.addressable_entity import AddressableEntityABC


class QueuableNotificationData(QueuableNotificationDataABC):
    def __init__(self, to_entity:List, to_entity_grp:List, to_entity_type:int, addressing_type:str, priority:int,
                    cb_url:str, cb_states:List[int]):
        self._to_entity=to_entity
        self._to_entity_grp=to_entity_grp
        self._to_entity_type=to_entity_type
        if self._to_entity_type not in list(zip(*AddrEntity.ENTITY_TYPE_CHOICES))[0]:
            raise IllegalArgumentError()
        self._addressing_type=self.AddressingType(addressing_type)
        self._priority=self.PriorityType(priority)
        self._cb_url=cb_url
        self._cb_states=cb_states

    def to_json(self):
        return super().to_json()

    def from_json(self):
        return super().from_json()

    def get_priority(self)->PriorityType:
        return self._priority
    
    def get_notifiaction_id(self):
        return super().get_notifiaction_id()
    
    def get_entity_ids(self):
        return super().get_entity_ids()
    
    def get_addressing_group_ids(self):
        return super().get_addressing_group_ids()
    
    def get_addressing_type(self):
        return super().get_addressing_type()
    
    def get_notification_content(self):
        return super().get_notification_content()
    def notification_cb_url(self)->str:
        return super().get_notification_content()
    def notification_cb_states(self)->List[int]:
        return super().get_notification_content()

class QueuableSmsNotificationData(QueuableNotificationData, RequestABC):
    class SmsType(enum.IntEnum):
        TRANSACTIONAL   = 3
        PROMOTIONAL     = 2
        OTP             = 1

    def __init__(self, n_id:str, from_phone:str, from_code:str,
                    sms_content:str, sms_type:SmsType,
                    to_entity:list, to_entity_grp:list, to_entity_type:int, addressing_type:str, priority:int,
                    cb_url:str, cb_states:List[int]):
        """
        *Returns SMS Queue Data*

        nid - Notification ID. Pass None if notification service shall generate
        from_phone - Phone number to use for sending this SMS (Used for promotional SMS only)

        from_code - SMS Code to use for sending this SMS (Used for Transactional/OTP SMS only)

        sms_content - SMS Text (Max 512 Chars)

        sms_type - Type of SMS. Possible values -
                        
                        1. TRANSACTIONAL   = 3
                        2. PROMOTIONAL     = 2
                        3. OTP             = 1

        addressing_type - Used to decide if to_entity is used or to_entity_grp. Possible values in -

                        1. ENTITY = 'entity'
                        2. ENTITY_GROUP = 'entity_grp'

        to_entity -  entity ID to send this SMS

        to_entity_grp - List of entity Groups IDs to sent this SMS. If List is empty no filtering on groups is done.

        to_entity_type - Used along with to_entity_grp. Possible values in

                        1. TYPE_CUSTOMER = 1
                        2. TYPE_DELIVERY_AGENT = 2
                        3. TYPE_MERCHANT = 3

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

        """
        super().__init__(to_entity, to_entity_grp, to_entity_type, addressing_type, priority, cb_url, cb_states)
        pass

    @classmethod
    def from_request(cls, request_data)->(QueuableNotificationDataABC, Error.ErrorInfo):
        addressing_type=cls.AddressingType(request_data.get('addressing_type'))
        if addressing_type == cls.AddressingType.ENTITY:
            if request_data.get('nid', None) is None:
                request_data['nid']=str(uuid.uuid4())
            return cls(request_data), Error.NO_ERROR


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
        self._eid=eid
        self._e_type=e_type
        self._phones=phones
        self._emails=emails
        self._fcm_tokens=fcm_tokens

    @classmethod
    def from_request(cls, request_data)->(AddressableEntityABC, Error.ErrorInfo):
        '''
        eid is mandatory (cannot be None)
        e_type is mandatory and has to be from valid choices
        phone, emails and fcm_tokens if not present or None is ignored when updating
        if present has to be list, and is set as it is
        '''
        try:
            eid=request_data.get('eid', None)
            e_type=request_data.get('e_type', None)
            phones=request_data.get('phones', None)
            emails=request_data.get('emails', None)
            fcm_tokens=request_data.get('fcm_tokens', None)
            if ((phones is None) or isinstance(phones, list)) and   \
            ((emails is None) or isinstance(emails, list)) and      \
            ((fcm_tokens is None) or isinstance(fcm_tokens, list)) :
                #(e_type in list(zip(*AddrEntity.ENTITY_TYPE_CHOICES))[0]):
                return cls(
                    uuid.UUID(eid), e_type,
                    phones, emails, fcm_tokens), Error.NO_ERROR
        except (ValueError, AttributeError) as e:
            # request_data None
            # invalid UUID
            # TODO: Log exception and suppress raise
            raise e
        return None, Error.INVALID_PARAMETERS

    def get_entity_id(self)->uuid.UUID:
        return self._eid

    def get_entity_type(self)->int:
        return self._e_type

    def get_phones(self)->List:
        return self._phones

    def get_emails(self)->List:
        return self._emails

    def get_fcm_tokens(self)->List:
        return self._fcm_tokens
