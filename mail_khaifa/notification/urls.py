from django.urls import include, re_path, path
from . import views

app_name = 'notification'

urlpatterns = [
    re_path(r'^sms/send/$', views.enqueue_sms, name='sms-send'),                                #Called to Send Sms
    re_path(r'^sms/send/bulk/$', views.enqueue_sms, name='sms-send'),                           #Called to Send Sms
    re_path(r'^email/send/$', views.enqueue_email, name='email-send'),                          #Called to Send Email
    re_path(r'^push/send/$', views.enqueue_push, name='push-send'),                             #Called to Push Notification
    re_path(r'^entity/', views.create_or_update_entity, name='create_or_update_entity'),        #Called to Create or update entity
    re_path(r'^cb/queue/', views.handle_enqued_notification, name='queue-cb'),                  #called by CP Queue with notification Data
    re_path(r'^cb/<slug:client_identifier>/', views.handle_external_svc_cb, name='ext_svc_cb'), #called by External services
]
