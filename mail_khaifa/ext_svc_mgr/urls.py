from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = []

sms_urlpatterns=[
    #Add client specific sms callbacks here
    path(r'cb/sms/msg91/', views.handle_sms_msg91_cb),             #CB from MSG91 for SMS
    path(r'cb/sms/twilio/', views.handle_sms_twilio_cb),           #CB from Twilio for SMS
]

email_urlpatterns=[
    #Add client specific email callbacks here
    path(r'cb/email/sendgrid/', views.handle_email_sendgrid_cb),   #CB from Sendgrid
]

urlpatterns+=(sms_urlpatterns+email_urlpatterns)
urlpatterns = format_suffix_patterns(urlpatterns)
