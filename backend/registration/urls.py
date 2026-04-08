# registration/urls.py
from django.urls import path
from .views import (
    ApplicantListCreateView,
    WebsiteRegistrationView,
    WhatsAppRegistrationView,
    USSDSimulationView,
    africastalking_ussd_callback,
    whatsapp_webhook,
    check_status_by_id,
    ApplicantDeleteView,
    AdminLoginView,
)

urlpatterns = [
    path('applicants/', ApplicantListCreateView.as_view(), name='applicant-list'),
    path('register/web/', WebsiteRegistrationView.as_view(), name='web-register'),
    path('register/whatsapp/', WhatsAppRegistrationView.as_view(), name='whatsapp-register'),
    path('register/ussd/simulate/', USSDSimulationView.as_view(), name='ussd-simulate'),
    path('ussd/callback/', africastalking_ussd_callback, name='ussd-callback'),
    path('whatsapp/webhook/', whatsapp_webhook, name='whatsapp-webhook'),
    path('check-status/<str:id_number>/', check_status_by_id, name='check-status'),
    path('applicants/<int:id>/', ApplicantDeleteView.as_view(), name='applicant-delete'),
    path('auth/admin-login/', AdminLoginView.as_view(), name='admin-login'),
]