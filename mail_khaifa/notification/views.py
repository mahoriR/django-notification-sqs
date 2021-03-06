import requests

from django.core.exceptions import MultipleObjectsReturned
from django.db.utils import IntegrityError
from rest_framework import generics, status
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from ext_svc_mgr.ext_svc_mgr import ExternalServiceManager

from common_utils.errors import Error

from .serializers.serializer import (
    QueuableSmsNotificationData, QueuableEmailNotificationData, QueuableNotificationData,
    QueuablePushNotificationData, AddressableEntity, QueuableNotificationState)

from .models import Notification, AddrEntity
from .queue_mgr import QueueWriter

from .serializers.model_serializers import AddrEntitySerializer

from .ext_svc_interfacer import ExternalServiceManager

@api_view(['POST'])
@permission_classes((AllowAny,))
def enqueue_sms(request):
    if request.method == 'POST':
        queue_data, error = QueuableSmsNotificationData.from_request(request.data)
        if error!=Error.NO_ERROR:
            return Response({'err':error}, status=status.HTTP_400_BAD_REQUEST)

        notification = Notification.insert_sms(
            queue_data.get_notifiaction_id(), queue_data.get_addr_entity(),
            queue_data.get_notification_cb_url(), queue_data.get_notification_cb_states())

        error = QueueWriter.enqueue_notification(queue_data)
        if error!=Error.NO_ERROR:
            return Response({'err':error}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'nid':str(queue_data.get_notifiaction_id())}, status=status.HTTP_200_OK)

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
        ExternalServiceManager.get_instance(QueueWriter).handle_enqued_notification_payload(request.data)
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny,))
def handle_external_svc_cb(request, client_identifier:str):
    if request.method == 'POST':
        state_transition=ExternalServiceManager.handle_callback(request.data, client_identifier)
        updated_state=state_transition.updated_state

        #Update DB
        notification=Notification.objects.get(ex_id=state_transition.external_id)
        notification=notification.update_state(updated_state, state_transition.external_id)
        cb_url=notification.get_notification_cb_url()
        cb_states=notification.get_notification_cb_states()

        if cb_url and (updated_state in cb_states):
            notification_state_cb=QueuableNotificationState(
                notification.get_notifiaction_id(), updated_state, cb_url, 0)
            #TBD : Check Errror
            QueueWriter.enqueue_notification_state_cb(notification_state_cb)
        return Response(status=status.HTTP_200_OK)
