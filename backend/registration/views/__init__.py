# registration/views/__init__.py
from .api_views import (
    ApplicantListCreateView,
    WebsiteRegistrationView,
    WhatsAppRegistrationView,
    USSDSimulationView,
    AdminLoginView,
)
from .ussd_views import africastalking_ussd_callback
from .whatsapp_views import whatsapp_webhook
from .status_views import check_status_by_id
from .root_view import root_view
from .Delete_view import ApplicantDeleteView

__all__ = [
    'ApplicantListCreateView',
    'WebsiteRegistrationView',
    'WhatsAppRegistrationView',
    'USSDSimulationView',
    'AdminLoginView',
    'africastalking_ussd_callback',
    'whatsapp_webhook',
    'check_status_by_id',
    'root_view',
    'ApplicantDeleteView',
]