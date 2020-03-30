from django.conf.urls import url, include
from . import views


"""
urlpatterns = [
    path(r'sms/send/', views.enqueue_sms),                          #Called to Send Sms
    path(r'email/send/', views.enqueue_email),                      #Called to Send Email
    path(r'push/send/', views.enqueue_push),                        #Called to Push Notification
    path(r'entity/', views.create_or_update_entity),                #Called to Create or update entity
    path(r'cb/data/', views.handle_enqued_notification),            #called by CP Queue with notification Data
    path(r'cb/state/', views.handle_enqued_notification_state_cb)   #called by CP Queue with notification State
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

"""
app_name = 'notification'

urlpatterns = [
    url(r'^sms/send/$', views.enqueue_sms, name='sms-send'),                            #Called to Send Sms
    url(r'^sms/send/bulk/$', views.enqueue_sms, name='sms-send'),                            #Called to Send Sms
    url(r'^email/send/$', views.enqueue_email, name='email-send'),                      #Called to Send Email
    url(r'^push/send/$', views.enqueue_push, name='push-send'),                         #Called to Push Notification
    url(r'entity/', views.create_or_update_entity, name='create_or_update_entity'),        #Called to Create or update entity
    url(r'cb/queue/', views.handle_enqued_notification, name='queue-cb'),               #called by CP Queue with notification Data
    #url(r'cb/state/', views.handle_enqued_notification_state_cb, name='push-send')     #called by CP Queue with notification State
]
