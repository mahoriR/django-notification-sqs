import abc, uuid, collections, enum, json
from typing import List, Dict

from common_utils.errors import Error
from common_utils.exceptions import IllegalArgumentError

from common_utils.interfaces.request_serializer import RequestABC

from ..models import AddrEntity, Notification

from ..interfaces.queuable_notification_data import QueuableNotificationDataABC
from ..interfaces.queuable_notification_state import QueuableNotificationStateABC
from ..interfaces.addressable_entity import AddressableEntityABC


class QueuableNotificationData(QueuableNotificationDataABC):
    def __init__(
        self, n_id:str, n_type:Notification.NotificationType, e_pk:int, to_entity:str=None, to_entity_type:AddrEntity.AddrEntityType=None,
        priority:QueuableNotificationDataABC.PriorityType=None, cb_url:str=None, cb_states:List[int]=None, max_ts:int=0):
        '''
        ** n_id - Notification ID.\n
        ** to_entity - eid for entity to whom notification has to be sent\n
        ** to_entity_type - Type of entity. Required as eid and type together uniquely identify addrEntity\n
        ** priority - notification priority\n
        ** cb_url - url to be called for notifying about state updates\n
        ** cb_states - states that require cb to be called\n
        ** max_ts - will not be sent after this. Ignored if 0\n
        '''

        if n_id is None:
            self._n_id = uuid.uuid4() #generate notification ID
        else: self._n_id = uuid.UUID(n_id)
        self._n_type=Notification.NotificationType(n_type)

        if e_pk is not None:
            self._addr_entity = AddrEntity.objects.get(pk=e_pk)
        else:
            to_entity_type=AddrEntity.AddrEntityType(to_entity_type)
            self._addr_entity = AddrEntity.objects.get(eid=uuid.UUID(to_entity), e_type=to_entity_type)

        self._priority=self.PriorityType(priority)
        self._cb_url=cb_url
        self._cb_states=cb_states or list()
        if not isinstance(self._cb_states, list):
            raise IllegalArgumentError('cb_states')
        self._max_ts=max_ts

    def to_dict(self)->Dict:
        return {
            'n_id':str(self.get_notifiaction_id()),
            'n_type':self._n_type,
            'e_pk':self._addr_entity.pk,
            'priority':self.get_priority(),
            'cb_url':self.get_notification_cb_url(),
            'cb_states':self.get_notification_cb_states(),
            'max_ts':self._max_ts
        }

    @classmethod
    def from_dict(cls, dict_data:Dict):
        '''
        Converts Json to QueuableNotificationData
        While from_request method performs checks, this assumes data is clean
        '''
        return cls(
            dict_data.get('nid'),
            dict_data.get('n_type'),
            dict_data.get('e_pk'),
            None, None,
            dict_data.get('priority'),
            dict_data.get('cb_url'),
            dict_data.get('cb_states'),
            dict_data.get('max_ts'))

    def get_addr_entity(self)->AddrEntity:
        return self._addr_entity

    def get_priority(self)->QueuableNotificationDataABC.PriorityType:
        return self._priority

    def get_notifiaction_id(self)->uuid.UUID:
        return self._n_id

    def get_notification_type(self)->int:
        return self._n_type

    def get_notification_cb_url(self)->str:
        return self._cb_url

    def get_notification_cb_states(self)->List[int]:
        return self._cb_states

    def get_max_timestamp(self)->int:
        return self._max_ts


class QueuableSmsNotificationData(QueuableNotificationData, RequestABC):
    class SmsType(enum.IntEnum):
        TRANSACTIONAL   = 3
        PROMOTIONAL     = 2
        OTP             = 1

    def __init__(
        self, n_id:str, n_type:Notification.NotificationType, e_pk:int, to_entity:str, to_entity_type:AddrEntity.AddrEntityType,
        priority:QueuableNotificationData.PriorityType, cb_url:str, cb_states:List[int], max_ts:int,
        from_phone:str, from_code:str, sms_text:str, sms_type:SmsType, template_name:str=None):
        """
        *Returns SMS Queue Data*\n\n
        nid - Notification ID. Pass None if notification service shall generate\n
        from_phone - Phone number to use for sending this SMS (Used for promotional SMS only)\n
        from_code - SMS Code to use for sending this SMS (Used for Transactional/OTP SMS only)\n
        sms_text - SMS Text (Max 512 Chars)\n
        sms_type - Type of SMS. Possible values -\n
                        1. TRANSACTIONAL   = 3
                        2. PROMOTIONAL     = 2
                        3. OTP             = 1
        template_name - Name of SMS template\n
        """
        super().__init__(n_id, n_type, e_pk, to_entity, to_entity_type, priority, cb_url, cb_states, max_ts)
        self._from_code=from_code
        self._from_phone=from_phone
        self._sms_text=sms_text
        self._sms_type=self.SmsType(sms_type)
        self._to_phones=self.get_addr_entity().get_phones()
        self._template_name=template_name

    def to_dict(self)->Dict:
        dict_data=super().to_dict()
        dict_data["payload"]=self.get_payload()
        return dict_data

    @classmethod
    def from_dict(cls, dict_data:Dict):
        payload=dict_data.pop('payload')
        return cls(**dict_data, **payload)

    def get_payload(self)->Dict:
        return {
            'from_code':self._from_code,
            'from_phone':self._from_phone,
            'to_phones':self._to_phones,
            'sms_type':self._sms_type,
            'sms_text':self._sms_text,
            'template_name':self._template_name
        }

    @classmethod
    def from_request(cls, request_data)->(QueuableNotificationDataABC, Error.ErrorInfo):

        try:
            return cls(
                request_data.get('n_id', None),
                Notification.NotificationType.TYPE_SMS,
                None,
                request_data['to_entity'],
                request_data['to_entity_type'],
                request_data['priority'],
                request_data.get('cb_url', None),
                request_data.get('cb_states', None),
                request_data.get('max_ts', 0),
                request_data.get('from_phone', None),
                request_data.get('from_code', None),
                request_data['sms_text'],
                request_data['sms_type'],
                request_data.get('template_name', None),
            ), Error.NO_ERROR
        except ValueError: # Illegal params, invalid values for params
            raise 
            return None, Error.INVALID_PARAMETERS
        except AttributeError: #if request data is None
            raise 
            return None, Error.INVALID_PARAMETERS
        except KeyError: #if mandatory keys are not present in request
            raise 
            return None, Error.INSUFFICIENT_PARAMETERS

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
    def __init__(self, n_id, n_state, cb_url, retry_count=0):
        self._n_state=Notification.NotificationState(n_state)
        self._n_id=uuid.UUID(n_id)
        self._retry_count=retry_count
        self._cb_url=cb_url
    
    def get_notification_state(self)->Notification.NotificationState:
        return self._n_state

    def get_notifiaction_id(self)->uuid.UUID:
        return self._n_id

    def get_retry_count(self)->int:
        return self._retry_count

    def set_retry_count(self, retry_count:int):
        self._retry_count=retry_count

    def get_notification_cb_url(self)->str:
        return self._cb_url

    def get_max_timestamp(self)->int:
        super().get_max_timestamp()
    
    def get_max_retry_count(self):
        return super().get_max_retry_count()

    def to_dict(self)->Dict:
        return {
            'n_state':self._n_state,
            'n_id':str(self._n_id),
            'retry_count':self._retry_count,
            'cb_url':self._cb_url
        }

    @classmethod
    def from_dict(cls, dict_data:Dict)->QueuableNotificationStateABC:
        return cls(**dict_data)

class AddressableEntity(AddressableEntityABC, RequestABC):
    def __init__(self, eid:uuid.UUID, e_type:AddrEntity.AddrEntityType, phones:List, emails:List, fcm_tokens:List):
        self._eid=eid
        self._e_type=AddrEntity.AddrEntityType(e_type)
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
            ((fcm_tokens is None) or isinstance(fcm_tokens, list)):
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

    def get_entity_type(self)->AddrEntity.AddrEntityType:
        return self._e_type

    def get_phones(self)->List[str]:
        return self._phones

    def get_emails(self)->List[str]:
        return self._emails

    def get_fcm_tokens(self)->List[str]:
        return self._fcm_tokens
