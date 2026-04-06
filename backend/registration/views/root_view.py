# registration/views/root_view.py
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        "message": "Voter Registration API is running",
        "endpoints": {
            "admin": "/admin/",
            "api_applicants": "/api/applicants/",
            "web_registration": "/api/register/web/",
            "whatsapp_registration": "/api/register/whatsapp/",
            "ussd_simulation": "/api/register/ussd/simulate/",
            "ussd_callback": "/api/ussd/callback/"
        }
    })