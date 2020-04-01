import json, uuid
from django.test import TestCase
from ..models import Notification, AddrEntity
from ..serializers.serializer import QueuableSmsNotificationData
from common_utils.errors import Error

class QueuableSmsNotificationDataTestCases(TestCase):
    """ Tests for QueuableSmsNotificationData serializer """

    def setUp(self):
        eid=uuid.uuid4()
        e_type=AddrEntity.AddrEntityType.TYPE_CUSTOMER
        addr_entity=AddrEntity.create(eid, e_type, phones=["+917829876765"])
        self.addr_entity=addr_entity

    def test_simple(self):
        request_data={
            'n_id':str(uuid.uuid4()),
            'to_entity':str(self.addr_entity.eid),
            'to_entity_type':self.addr_entity.e_type,
            'priority':1,
            'cb_url':"svc://customer/cb",
            'cb_states':[Notification.NotificationState.STATE_FAILED],
            'max_ts':9,
            'from_phone':["+917898787656"],
            'from_code':"FMCODE",
            'sms_text':"Hello World!",
            'sms_type':QueuableSmsNotificationData.SmsType.TRANSACTIONAL,
            'template_name':"template-one-name",
        }
        data, error=QueuableSmsNotificationData.from_request(request_data)
        self.assertEqual(error, Error.NO_ERROR)
        self.assertEqual(data.get_payload(), {
            'from_code':request_data['from_code'],
            'from_phone':request_data['from_phone'],
            'to_phones':self.addr_entity.get_phones(),
            'sms_type':request_data['sms_type'],
            'sms_text':request_data['sms_text'],
            'template_name':request_data['template_name']
        })
