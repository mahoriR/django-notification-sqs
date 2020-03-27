import json, uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


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
        print(response.data)
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
        print(response.data)
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
        print(response.data)
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
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
