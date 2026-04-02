from django.urls import path
from .views import (
    ApplicantListCreateView,
    WebsiteRegistrationView,
    WhatsAppRegistrationView,
    USSDSimulationView,
    AfricaTalkingUSSDRedirect
)

urlpatterns = [
    # Admin/listing API
    path('applicants/', ApplicantListCreateView.as_view(), name='applicant-list'),
    
    # Channel-specific registration endpoints
    path('register/web/', WebsiteRegistrationView.as_view(), name='web-register'),
    path('register/whatsapp/', WhatsAppRegistrationView.as_view(), name='whatsapp-register'),
    path('register/ussd/simulate/', USSDSimulationView.as_view(), name='ussd-simulate'),
    
    # Africa's Talking USSD webhook (production)
    path('ussd/callback/', AfricaTalkingUSSDRedirect.as_view(), name='ussd-callback'),
]