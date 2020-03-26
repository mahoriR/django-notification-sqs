from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path(r'sms/send/', views.enqueue_sms),                          #Called to Send Sms
    path(r'email/send/', views.enqueue_email),                      #Called to Send Email
    path(r'push/send/', views.enqueue_push),                        #Called to Push Notification
    path(r'entity/', views.create_or_update_entity),                #Called to Create or update entity

    path(r'cb/data/', views.handle_enqued_notification),            #called by CP Queue with notification Data
    path(r'cb/state/', views.handle_enqued_notification_state_cb)   #called by CP Queue with notification State
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

