from mail_khaifa.cp_utils.errors import CpError

from mail_khaifa.ext_svc_mgr.ext_svc_mgr import ExternalServiceManager

from ..serializer import (
    QueuableSmsNotificationData, QueuableEmailNotificationData, QueuableNotificationData,
    QueuablePushNotificationData, AddressableEntity)

from ..models import Notification
from ..queue_mgr import QueueWriter


@api_view(['POST'])
def enqueue_sms(request):
    if request.method == 'POST':
        queue_data, cp_error = QueuableSmsNotificationData.from_request(request.data)
        if cp_error!=CpError.NO_ERROR:
            return Response({'err_mess':cp_error.message, 'err_code':cp_error.code}, status=status.HTTP_400_BAD_REQUEST)

        if queue_data.get_addressing_type()==QueuableSmsNotificationData.AddressingType.ENTITY:
            notification = Notification.insert_sms(queue_data.get_notifiaction_id(), queue_data.get_entity_ids()[0])
        else: raise NotImplementedError()

        cp_error = QueueWriter.enqueue_notification(queue_data.get_priority(),  queue_data.to_json())
        if cp_error!=CpError.NO_ERROR:
            return Response({'err_mess':cp_error.message, 'err_code':cp_error.code}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'nid':queue_data.get_notifiaction_id()}, status=status.HTTP_200_OK)

@api_view(['POST'])
def enqueue_email(request):
    if request.method == 'POST':
        pass

        return Response(content, status=status.HTTP_200_OK)

@api_view(['POST'])
def enqueue_push(request):
    if request.method == 'POST':
        pass

        return Response(content, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_or_update_entity(request):
    if request.method == 'POST':
        entity_data, cp_error = AddressableEntity.from_request(request.data)

        return Response(content, status=status.HTTP_200_OK)

@api_view(['POST'])
def handle_enqued_notification(request):
    if request.method == 'POST':
        queue_data, cp_error = QueuableNotificationData.from_json(request.data)
        if queue_data.get_notifiaction_type()==Notification.TYPE_SMS:

            # Handle the Request to Send SMS
            queue_data, cp_error = QueuableSmsNotificationData.from_json(request.data)
            result=ExternalServiceManager.send(queue_data)

            #Update DB with state
            updated_state=Notification.STATE_FAILED
            external_id=None
            if result.is_success():
                updated_state=Notification.STATE_SENT
                external_id=result.get_external_id()

            #Update DB
            Notification=Notification.update_state(updated_state, external_id)

            if updated_state in queue_data.notification_cb_states():
                #Enqueue Callback for Sent, if required
                notification_state_cb=QueuableNotificationState(
                    updated_state, queue_data.get_notifiaction_id(),
                    queue_data.notification_cb_url(), queue_data.notification_cb_states(), 0)
                #TBD: Check Errror
                QueueWriter.enqueue_notification_state_cb(notification_state_cb)
        else:
            raise NotImplementedError()

        return Response(content, status=status.HTTP_200_OK)


@api_view(['POST'])
def handle_enqued_notification_state_cb(request):
    if request.method == 'POST':
        raise NotImplementedError()

        return Response(content, status=status.HTTP_200_OK)