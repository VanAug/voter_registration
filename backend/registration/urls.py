# registration/urls.py
from django.urls import path
from .views import (
    ApplicantListCreateView,
    WebsiteRegistrationView,
    WhatsAppRegistrationView,
    USSDSimulationView,
    africastalking_ussd_callback,
    whatsapp_webhook
)

urlpatterns = [
    path('applicants/', ApplicantListCreateView.as_view(), name='applicant-list'),
    path('register/web/', WebsiteRegistrationView.as_view(), name='web-register'),
    path('register/whatsapp/', WhatsAppRegistrationView.as_view(), name='whatsapp-register'),
    path('register/ussd/simulate/', USSDSimulationView.as_view(), name='ussd-simulate'),
    path('ussd/callback/', africastalking_ussd_callback, name='ussd-callback'),
    path('whatsapp/webhook/', whatsapp_webhook, name='whatsapp-webhook'),
]