from django.core.exceptions import MultipleObjectsReturned
from django.db.utils import IntegrityError
from rest_framework import generics, status
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ParseError

from ext_svc_mgr.ext_svc_mgr import ExternalServiceManager

from common_utils.errors import Error

from .serializers.serializer import (
    QueuableSmsNotificationData, QueuableEmailNotificationData, QueuableNotificationData,
    QueuablePushNotificationData, AddressableEntity)

from .models import Notification, AddrEntity
from .queue_mgr import QueueWriter

from .serializers.model_serializers import AddrEntitySerializer

@api_view(['POST'])
@permission_classes((AllowAny,))
def enqueue_sms(request):
    if request.method == 'POST':
        queue_data, error = QueuableSmsNotificationData.from_request(request.data)
        if error!=Error.NO_ERROR:
            return Response({'err':error}, status=status.HTTP_400_BAD_REQUEST)

        if queue_data.get_addressing_type()==QueuableSmsNotificationData.AddressingType.ENTITY:
            notification = Notification.insert_sms(queue_data.get_notifiaction_id(), queue_data.get_entity_ids()[0])
        else: raise NotImplementedError()

        error = QueueWriter.enqueue_notification(queue_data.get_priority(), queue_data.to_json())
        if error!=Error.NO_ERROR:
            return Response({'err':error}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'nid':queue_data.get_notifiaction_id()}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny,))
def enqueue_sms_bulk(request):
    if request.method == 'POST':
        queue_data, error = QueuableSmsNotificationData.from_request(request.data)
        if error!=Error.NO_ERROR:
            return Response({'err':error}, status=status.HTTP_400_BAD_REQUEST)

        if queue_data.get_addressing_type()==QueuableSmsNotificationData.AddressingType.ENTITY:
            notification = Notification.insert_sms(queue_data.get_notifiaction_id(), queue_data.get_entity_ids()[0])
        else: raise NotImplementedError()

        error = QueueWriter.enqueue_notification(queue_data.get_priority(), queue_data.to_json())
        if error!=Error.NO_ERROR:
            return Response({'err':error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@permission_classes((AllowAny,))
def enqueue_email(request):
    if request.method == 'POST':
        pass

        return Response(content, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny,))
def enqueue_push(request):
    if request.method == 'POST':
        pass

        return Response(content, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny,))
def create_or_update_entity(request):
    error=Error.UNKNOWN_ERROR
    if request.method == 'POST':
        try:
            entity_data, cp_error = AddressableEntity.from_request(request.data)
            if cp_error!=Error.NO_ERROR:
                return Response({'err':cp_error}, status=status.HTTP_400_BAD_REQUEST)
            #if entity exists, update
            #else create
            if AddrEntity.objects.filter(eid=entity_data.get_entity_id()).exists():
                #update
                addr_entity=AddrEntity.objects.get(eid=entity_data.get_entity_id())
                addr_entity=addr_entity.update(
                    phones=entity_data.get_phones(),
                    emails=entity_data.get_emails(),
                    fcm_tokens=entity_data.get_fcm_tokens())
                return Response(AddrEntitySerializer(addr_entity, many=False).data, status=status.HTTP_200_OK)

            #Create new
            addr_entity=AddrEntity.create(
                    eid=entity_data.get_entity_id(),
                    e_type=entity_data.get_entity_type(),
                    phones=entity_data.get_phones(),
                    emails=entity_data.get_emails(),
                    fcm_tokens=entity_data.get_fcm_tokens())
            return Response(AddrEntitySerializer(addr_entity, many=False).data, status=status.HTTP_201_CREATED)
        #django.db.utils.IntegrityError -> django.db.utils.IntegrityError: null value in column "e_type" violates not-null constraint
        #ValueError -> ValueError: Field 'e_type' expected a number but got '3f6078e8-b34e-43db-936c-abc83912cb99'
        except ValueError as e:
            #TODO: Log Exception
            error=Error.INVALID_PARAMETERS
        except IntegrityError as e:
            #TODO: Log Exception
            error=Error.INVALID_PARAMETERS
        return Response({'err':error}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((AllowAny,))
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
@permission_classes((AllowAny,))
def handle_enqued_notification_state_cb(request):
    if request.method == 'POST':
        raise NotImplementedError()

        return Response(content, status=status.HTTP_200_OK)