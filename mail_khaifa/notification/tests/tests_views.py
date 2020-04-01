import json, uuid, time
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Notification, AddrEntity

class CreateUpdateEntity(APITestCase):
    """ Test module for Create Entity """
    url = reverse("notification:create_or_update_entity")
    fixed_uuid='7a85e49b-66dd-48df-a92f-1f9e84263d15'

    def test_create_entity_minimal(self):
        self.valid_payload={
            'eid':str(uuid.uuid4()),
            'e_type':1
        }
        response = self.client.post(
            self.url, data=json.dumps(self.valid_payload),
            content_type='application/json')
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_entity_complete(self):
        self.valid_payload={
            'eid':str(uuid.UUID(self.fixed_uuid)),
            'e_type':1,
            'phones':['+917829862689'],
            'emails':['ravinder@changepay.in'],
            'fcm_tokens':['+917829862689'],
        }
        response = self.client.post(
            self.url, data=json.dumps(self.valid_payload),
            content_type='application/json')
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_entity(self):
        self.valid_payload={
            'eid':str(uuid.UUID(self.fixed_uuid)),
            'e_type':1,
            'phones':['+917829862689'],
            'emails':['ravinder@changepay.in'],
            'fcm_tokens':['+917829862689'],
        }
        response = self.client.post(
            self.url, data=json.dumps(self.valid_payload),
            content_type='application/json')
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #Update
        self.valid_payload={
            'eid':str(uuid.UUID(self.fixed_uuid)),
            'e_type':1,
            'emails':['ravindernitks@gmail.com', 'ravinder@changepay.in'],
        }
        response = self.client.post(
            self.url, data=json.dumps(self.valid_payload),
            content_type='application/json')
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_neg_create_entity_minimal(self):
        self.valid_payload={
            'eid':str(uuid.uuid4()),
            'e_type':6
        }
        response = self.client.post(
            self.url, data=json.dumps(self.valid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class NotificationSMSTestCases(APITestCase):
    """ Test module for Notification """
    url = reverse("notification:sms-send")
    fixed_uuid='7a85e49b-66dd-48df-a92f-1f9e84263d15'

    def setUp(self):
        self.eid=str(uuid.uuid4())
        self.e_type=AddrEntity.AddrEntityType.TYPE_CUSTOMER
        self.valid_payload={
            'eid':self.eid,
            'e_type':self.e_type
        }
        response = self.client.post(
            reverse("notification:create_or_update_entity"), data=json.dumps(self.valid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_sms_minimal(self):
        self.valid_payload={
            'n_type':Notification.NotificationType.TYPE_SMS,
            'to_entity':self.eid,
            'to_entity_type':self.e_type,
            'priority':1,
            'sms_text':"Hello SMS World!",
            'sms_type':1,
        }
        response = self.client.post(
            self.url, data=json.dumps(self.valid_payload),
            content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_sms_complete(self):
        ni_d=str(uuid.uuid4())
        self.valid_payload={
            'n_id':ni_d,
            'to_entity':self.eid,
            'to_entity_type':self.e_type,
            'priority':1,
            'cb_url':'svc://customer/cb/notif',
            'cb_states':[Notification.NotificationState.STATE_SENT, Notification.NotificationState.STATE_FAILED],
            'max_ts':int(time.time())+5000,
            'from_phone':"+917829876435",
            'from_code':"FMCODE",
            'sms_text':"Hello SMS World!",
            'sms_type':1,
            'template_name':'template-otp-1'
        }
        response = self.client.post(
            self.url, data=json.dumps(self.valid_payload),
            content_type='application/json')
        print(response.data)
        self.assertEqual(response.data['nid'], ni_d)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
