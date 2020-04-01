import json, uuid
from django.test import TestCase
from ..models import Notification, AddrEntity
from common_utils.exceptions import IllegalArgumentError

class AddrEntityTestCases(TestCase):
    """ Tests for Addr Entity model """

    def test_insert_addr_entity_simple(self):
        eid=uuid.uuid4()
        e_type=AddrEntity.AddrEntityType.TYPE_CUSTOMER
        addr_entity=AddrEntity.create(eid, e_type)
        self.assertEqual(eid, addr_entity.eid)
        self.assertEqual(e_type, addr_entity.e_type)
        self.assertEqual([], addr_entity.get_phones()+addr_entity.get_fcm_tokens()+addr_entity.get_emails())

    def test_insert_addr_entity_complete(self):
        eid=uuid.uuid4()
        e_type=AddrEntity.AddrEntityType.TYPE_CUSTOMER
        phones=['+917829862689']
        emails=['ravinder@changepay.in']
        fcm_tokens=['xyazcv-fcm-token']
        addr_entity=AddrEntity.create(eid, e_type, phones, emails, fcm_tokens)
        self.assertEqual(eid, addr_entity.eid)
        self.assertEqual(e_type, addr_entity.e_type)
        self.assertEqual(phones, addr_entity.get_phones())
        self.assertEqual(emails, addr_entity.get_emails())
        self.assertEqual(fcm_tokens, addr_entity.get_fcm_tokens())

    def test_insert_addr_enttity_update(self):
        eid=uuid.uuid4()
        e_type=AddrEntity.AddrEntityType.TYPE_CUSTOMER
        addr_entity=AddrEntity.create(eid, e_type)
        phones=['+917829862689']
        emails=['ravinder@changepay.in']
        fcm_tokens=['xyazcv-fcm-token']
        addr_entity=addr_entity.update(phones, emails, fcm_tokens)
        self.assertEqual(eid, addr_entity.eid)
        self.assertEqual(e_type, addr_entity.e_type)
        self.assertEqual(phones, addr_entity.get_phones())
        self.assertEqual(emails, addr_entity.get_emails())
        self.assertEqual(fcm_tokens, addr_entity.get_fcm_tokens())

class NotificationTestCases(TestCase):
    """ Tests for notification model """

    def setUp(self):
        eid=uuid.uuid4()
        e_type=AddrEntity.AddrEntityType.TYPE_CUSTOMER
        addr_entity=AddrEntity.create(eid, e_type)
        self.addr_entity=addr_entity

    def test_insert_notification(self):
        nid=uuid.uuid4()
        eid=uuid.uuid4()
        n_type=Notification.NotificationType.TYPE_SMS
        notification = Notification.insert_notification(
            nid, self.addr_entity, n_type, None, None)
        self.assertEqual(nid, notification.nid)
        self.assertEqual(self.addr_entity.eid, notification.addr_entity.eid)
        self.assertEqual(n_type, notification.n_type)
        self.assertEqual(Notification.NotificationState.STATE_QUEUED, notification.n_state)
        self.assertEqual(0, notification.u_cancelled)
        self.assertEqual(None, notification.ex_id)
        self.assertEqual(None, notification.get_cb_path())
        self.assertEqual(None, notification.get_cb_states())

    def test_insert_sms(self):
        nid=uuid.uuid4()
        eid=uuid.uuid4()
        cb_path="customer://notif/cb/"
        cb_states=[Notification.NotificationState.STATE_FAILED, Notification.NotificationState.STATE_DELIVERED]
        notification = Notification.insert_sms(
            nid, self.addr_entity, cb_path, cb_states)
        self.assertEqual(nid, notification.nid)
        self.assertEqual(self.addr_entity.eid, notification.addr_entity.eid)
        self.assertEqual(Notification.NotificationType.TYPE_SMS, notification.n_type)
        self.assertEqual(Notification.NotificationState.STATE_QUEUED, notification.n_state)
        self.assertEqual(0, notification.u_cancelled)
        self.assertEqual(None, notification.ex_id)
        self.assertEqual(cb_path, notification.get_cb_path())
        self.assertEqual(cb_states, notification.get_cb_states())

    def test_update_state(self):
        nid=uuid.uuid4()
        eid=uuid.uuid4()
        notification = Notification.insert_sms(
            nid, self.addr_entity)
        updated_state=Notification.NotificationState.STATE_FAILED
        external_id="external-id-Fac78"
        notification=notification.update_state(updated_state, external_id)
        self.assertEqual(nid, notification.nid)
        self.assertEqual(self.addr_entity.eid, notification.addr_entity.eid)
        self.assertEqual(Notification.NotificationType.TYPE_SMS, notification.n_type)
        self.assertEqual(updated_state, notification.n_state)
        self.assertEqual(0, notification.u_cancelled)
        self.assertEqual(external_id, notification.ex_id)
        self.assertEqual(None, notification.get_cb_path())
        self.assertEqual(None, notification.get_cb_states())

    def test_neg_update_state(self):
        nid=uuid.uuid4()
        eid=uuid.uuid4()
        notification = Notification.insert_sms(
            nid, self.addr_entity)
        updated_state=Notification.NotificationState.STATE_FAILED+88
        external_id="external-id-Fac78"
        with self.assertRaises(ValueError):
            notification=notification.update_state(updated_state, external_id)
