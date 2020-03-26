import json, base64, uuid
from datetime import timedelta

from django.db import models, IntegrityError
from django.contrib.postgres.fields import JSONField


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

    eid = models.UUIDField(
        'Entity Id', primary_key=True)
    e_type = models.PositiveIntegerField(choices=ENTITY_TYPE_CHOICES)
    profile = JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
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

    nid = models.UUIDField('Notification Id', primary_key=True)
    eid =  models.ForeignKey(
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

    def __str__(self):
        return '{0} - {1}'.format(str(self.nid), str(self.n_type))

    @classmethod
    def insert_notification(cls, nid, eid, n_type):
        notification = cls(nid=nid, eid=eid, n_type=n_type, n_state=cls.STATE_QUEUED, u_cancelled=0, ex_id=None)
        notification.save()
        return notification

    @classmethod
    def insert_sms(cls, nid, eid):
        return cls.insert_notification(nid, eid, cls.TYPE_SMS)

    @classmethod
    def update_state(cls, state, external_id=None):
        raise NotImplementedError()

