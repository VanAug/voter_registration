# registration/views/status_views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from ..models import Applicant

@require_http_methods(["GET"])
def check_status_by_id(request, id_number):
    try:
        applicant = Applicant.objects.get(id_number=id_number)
        data = {
            'full_name': applicant.full_name,
            'phone_number': applicant.phone_number,
            'county': applicant.county,
            'voter_status': applicant.voter_status,
            'registration_channel': applicant.registration_channel,
            'registered_at': applicant.registered_at.isoformat()
        }
        return JsonResponse({'found': True, 'data': data})
    except Applicant.DoesNotExist:
        return JsonResponse({'found': False, 'message': 'No registration found with this ID number.'})