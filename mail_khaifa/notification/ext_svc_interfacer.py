import requests

from ext_svc_mgr.ext_svc_mgr import ExternalServiceManager

from common_utils.errors import Error

from .serializers.serializer import (
    QueuableSmsNotificationData, QueuableEmailNotificationData, QueuableNotificationData,
    QueuablePushNotificationData, AddressableEntity, QueuableNotificationState)

from .models import Notification, AddrEntity
#from .queue_mgr import QueueWriter


class ExternalSvcInterfacer(object):
    instance=None

    @classmethod
    def get_instance(cls, queue_writer):
        if cls.instance is None:
            cls.instance=cls(queue_writer)
        return cls.instance

    def __init__(self, queue_writer):
        self._queue_writer=queue_writer

    def handle_notification_data_from_queue(self, queue_data_payload):
        queue_data = QueuableNotificationData.from_dict(queue_data_payload)

        if queue_data.get_notification_type()==Notification.NotificationType.TYPE_SMS:
            NotifClass=QueuableSmsNotificationData
        elif queue_data.get_notification_type()==Notification.NotificationType.TYPE_EMAIL:
            raise NotImplementedError()
        elif queue_data.get_notification_type()==Notification.NotificationType.TYPE_PUSH:
            raise NotImplementedError()
        else:
            raise RuntimeError('Unknown Notification Type: '+str(queue_data.get_notifiaction_type()))

        queue_data = NotifClass.from_dict(queue_data_payload)
        result=ExternalServiceManager.send(queue_data)

        #Update DB with state
        updated_state=Notification.NotificationState.STATE_FAILED
        external_id=None
        if result.is_success:
            updated_state=Notification.NotificationState.STATE_SENT
            external_id=result.external_id

        #Update DB
        notification=Notification.objects.get(nid=queue_data.get_notifiaction_id())
        notification=notification.update_state(updated_state, external_id)

        if queue_data.get_notification_cb_url() and (updated_state in queue_data.get_notification_state()):
            notification_state_cb=QueuableNotificationState(
                queue_data.get_notifiaction_id(), updated_state, queue_data.get_notification_cb_url(), 0)
            #TBD : Check Errror
            self._queue_writer.enqueue_notification_state_cb(notification_state_cb)

    def handle_notification_state_from_queue(self, queue_state_payload):
        #Call external Service. If call fails, reque.
        notification_state_cb=QueuableNotificationState.from_dict(queue_state_payload)
        r=requests.post(notification_state_cb.get_notification_cb_url(), data={'state':notification_state_cb.get_notification_state()})
        if (r.status_code != requests.codes.ok) and (notification_state_cb.get_retry_count() < notification_state_cb.get_max_retry_count()):
            #requeue if retry count not already exceed 3?
            notification_state_cb.set_retry_count(notification_state_cb.get_retry_count()+1)
            self._queue_writer.enqueue_notification_state_cb(notification_state_cb)

    def handle_enqued_notification_payload(self, payload_data):
        queued_payload, q_entity_type=self._queue_writer.get_payload_and_type(payload_data)
        if q_entity_type==self._queue_writer.QueuedEntityType.DATA:
            self.handle_notification_data_from_queue(queued_payload)
        elif q_entity_type==self._queue_writer.QueuedEntityType.STATE:
            self.handle_notification_state_from_queue(queued_payload)
        else:
            raise RuntimeError('Invalid Queued Entity Type '+q_entity_type)