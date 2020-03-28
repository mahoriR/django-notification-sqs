from typing import List
import json, base64, uuid
from datetime import timedelta

from django.db import models, IntegrityError
from django.contrib.postgres.fields import JSONField

from common_utils.exceptions import IllegalArgumentError

class AddrEntity(models.Model):
    '''
    Addressable entities in Changepay System
    '''

    TYPE_CUSTOMER = 1
    TYPE_DELIVERY_AGENT = 2
    TYPE_MERCHANT = 3

    ENTITY_TYPE_CHOICES = (
        (TYPE_CUSTOMER, 'Customer'),
        (TYPE_DELIVERY_AGENT, 'Delivery Agent'),
        (TYPE_MERCHANT, 'Merchant'),
        )
    
    CONST_KEY_PHONES="ph"
    CONST_KEY_EMAILS="em"
    CONST_KEY_FCM_TOKENS="ft"

    eid = models.UUIDField(
        'Entity Id', primary_key=True)
    e_type = models.PositiveIntegerField(choices=ENTITY_TYPE_CHOICES)
    profile = JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)

    @classmethod
    def create(cls, eid, e_type, phones=None, emails=None, fcm_tokens=None):
        phones,emails,fcm_tokens=phones or [],emails or [],fcm_tokens or []
        profile={
            cls.CONST_KEY_PHONES:phones,
            cls.CONST_KEY_EMAILS:emails,
            cls.CONST_KEY_FCM_TOKENS:fcm_tokens,
            }
        addr_entity = cls(eid=eid, e_type=e_type, profile=profile)
        addr_entity.save()
        return addr_entity

    def update(self, phones=None, emails=None, fcm_tokens=None):
        profile=self.profile
        if phones is not None:
            profile[self.CONST_KEY_PHONES]=phones
        if emails is not None:
            profile[self.CONST_KEY_EMAILS]=emails
        if fcm_tokens is not None:
            profile[self.CONST_KEY_FCM_TOKENS]=fcm_tokens
        self.profile=profile
        self.save()
        return self

    def get_phones(self):
        return self.profile[self.CONST_KEY_PHONES]
    def get_emails(self):
        return self.profile[self.CONST_KEY_EMAILS]
    def get_fcm_tokens(self):
        return self.profile[self.CONST_KEY_FCM_TOKENS]

    def __str__(self): # pragma: no cover
        return '{0} - {1}'.format(str(self.eid), str(self.e_type))

class Notification(models.Model):
    '''
    Notifications.
    '''

    TYPE_SMS = 1
    TYPE_EMAIL = 2
    TYPE_PUSH = 3

    NOTIFICATION_TYPE_CHOICES = (
        (TYPE_SMS, 'Sms'),
        (TYPE_EMAIL, 'Email'),
        (TYPE_PUSH, 'Push (Android/iOS)'),
        )

    STATE_QUEUED = 1
    STATE_SENT = 2
    STATE_DELIVERED = 3
    STATE_READ = 4
    STATE_FAILED = 5

    NOTIFICATION_STATE_CHOICES = (
        (STATE_QUEUED, 'Queued'),
        (STATE_SENT, 'Sent'),
        (STATE_DELIVERED, 'Delivered'),
        (STATE_READ, 'Read'),
        (STATE_FAILED, 'Failed'),
        )

    CONST_KEY_CB_PATH="cbp"
    CONST_KEY_CB_STATES="cbs"

    nid = models.UUIDField('Notification Id', primary_key=True)
    addr_entity =  models.ForeignKey(
        AddrEntity, on_delete=models.SET_NULL, blank=True, null=True,
    )
    n_type = models.PositiveIntegerField(choices=NOTIFICATION_TYPE_CHOICES)
    n_state = models.PositiveIntegerField(choices=NOTIFICATION_STATE_CHOICES)

    #User cancelled?
    u_cancelled = models.PositiveIntegerField(default=0)

    #external ID
    ex_id = models.CharField(max_length=512, null=True, unique=True)
    #Stores Callback info as List of States and CB_URL
    cb_info = JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self): # pragma: no cover
        return '{0} - {1}'.format(str(self.nid), str(self.n_type))

    @classmethod
    def insert_notification(cls, nid:uuid.UUID, addr_entity:AddrEntity, n_type:int, cb_path:str, cb_states:List[int]):
        cb_info={
            cls.CONST_KEY_CB_PATH:cb_path,
            cls.CONST_KEY_CB_STATES:cb_states
        }
        notification = cls(nid=nid, addr_entity=addr_entity, n_type=n_type, n_state=cls.STATE_QUEUED, u_cancelled=0, ex_id=None, cb_info=cb_info)
        notification.save()
        return notification

    @classmethod
    def insert_sms(cls, nid:uuid.UUID, addr_entity:AddrEntity, cb_path:str=None, cb_states:List[int]=None):
        return cls.insert_notification(nid, addr_entity, cls.TYPE_SMS, cb_path, cb_states)

    def update_state(self, state:int, external_id:str):
        if state not in list(zip(*self.NOTIFICATION_STATE_CHOICES))[0]:
            raise IllegalArgumentError()
        self.n_state=state
        self.ex_id=external_id
        self.save()
        return self

    def get_cb_states(self):
        return self.cb_info.get(self.CONST_KEY_CB_STATES)

    def get_cb_path(self):
        return self.cb_info.get(self.CONST_KEY_CB_PATH)
