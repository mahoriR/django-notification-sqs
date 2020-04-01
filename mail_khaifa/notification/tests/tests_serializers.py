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

        self.assertEqual(data.get_addr_entity(), self.addr_entity)
        self.assertEqual(data.get_priority(), request_data['priority'])
        self.assertEqual(data.get_notifiaction_id(), uuid.UUID(request_data['n_id']))
        self.assertEqual(data.get_notification_type(), Notification.NotificationType.TYPE_SMS)
        self.assertEqual(data.get_notification_cb_url(), request_data['cb_url'])
        self.assertEqual(data.get_notification_cb_states(), request_data['cb_states'])
        self.assertEqual(data.get_max_timestamp(), request_data['max_ts'])

        dict_payload={
            'from_code':request_data['from_code'],
            'from_phone':request_data['from_phone'],
            'to_phones':self.addr_entity.get_phones(),
            'sms_type':request_data['sms_type'],
            'sms_text':request_data['sms_text'],
            'template_name':request_data['template_name']
        }
        self.assertEqual(data.get_payload(), dict_payload)
        data_dict={
            'payload':dict_payload,
            'n_id':request_data['n_id'],
            'n_type':Notification.NotificationType.TYPE_SMS,
            'e_pk':self.addr_entity.pk,
            'priority':request_data['priority'],
            'cb_url':request_data['cb_url'],
            'cb_states':request_data['cb_states'],
            'max_ts':request_data['max_ts']
        }
        self.assertEqual(data.to_dict(), data_dict)
        #round trip complete!
        self.assertEqual(data.to_dict(), QueuableSmsNotificationData.from_dict(data_dict).to_dict())
