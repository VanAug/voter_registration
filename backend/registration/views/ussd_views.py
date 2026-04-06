# registration/views/ussd_views.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from ..models import Applicant, RegistrationChannel
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def africastalking_ussd_callback(request):
    try:
        session_id = request.POST.get("sessionId")
        phone_number = request.POST.get("phoneNumber", "").strip()
        text = request.POST.get("text", "")

        if phone_number and not phone_number.startswith('+'):
            phone_number = '+' + phone_number

        cache_key = f"ussd_{session_id}"
        session_data = cache.get(cache_key, {})

        print(f"USSD: session={session_id}, phone={phone_number}, text='{text}', data={session_data}")

        if text == "":
            cache.delete(cache_key)
            response = "CON Welcome to Voter Registration\n1. Register To Vote\n2. Check Voter Status\n0. Exit"
            return HttpResponse(response, content_type="text/plain")

        parts = text.split('*')
        level = len(parts)
        choice = parts[0]

        if choice == "1":
            if level == 1:
                session_data = {'step': 'name'}
                cache.set(cache_key, session_data, timeout=300)
                response = "CON Enter your full name:"
            elif level == 2:
                session_data['name'] = parts[1].strip()
                session_data['step'] = 'id'
                cache.set(cache_key, session_data, timeout=300)
                response = "CON Enter your ID number:"
            elif level == 3:
                id_num = parts[2].strip()
                id_num = ''.join(filter(str.isdigit, id_num))
                session_data['id_number'] = id_num
                session_data['step'] = 'county'
                cache.set(cache_key, session_data, timeout=300)
                response = "CON Enter your county of residence:"
            elif level == 4:
                session_data['county'] = parts[3].strip()
                session_data['step'] = 'voter'
                cache.set(cache_key, session_data, timeout=300)
                response = "CON Do you wish to register as a voter?\n1. Yes\n2. No"
            elif level == 5:
                voter_choice = parts[4].strip()
                voter_status = (voter_choice == "1")
                name = session_data.get('name', '')
                id_num = session_data.get('id_number', '')
                county = session_data.get('county', '')

                if not name or not id_num or not county:
                    response = "END Registration failed: missing data. Please restart."
                else:
                    phone_exists = Applicant.objects.filter(phone_number=phone_number).exists()
                    id_exists = Applicant.objects.filter(id_number=id_num).exists()
                    if phone_exists:
                        response = "END This phone number is already registered."
                    elif id_exists:
                        response = "END This ID number is already registered."
                    else:
                        try:
                            applicant = Applicant.objects.create(
                                full_name=name,
                                phone_number=phone_number,
                                id_number=id_num,
                                county=county,
                                voter_status=voter_status,
                                registration_channel=RegistrationChannel.USSD
                            )
                            response = f"END Registration successful! Welcome {applicant.full_name}."
                        except Exception as e:
                            print(f"Save error: {e}")
                            response = "END An internal error occurred. Please try again."
                cache.delete(cache_key)
            else:
                response = "END Too many steps. Restart."
            return HttpResponse(response, content_type="text/plain")

        elif choice == "2":
            if level == 1:
                response = "CON Enter your ID number:"
            elif level == 2:
                id_num = parts[1].strip()
                id_num = ''.join(filter(str.isdigit, id_num))
                try:
                    applicant = Applicant.objects.get(id_number=id_num)
                    status_text = "Yes" if applicant.voter_status else "No"
                    response = (
                        f"END Registration Details:\n"
                        f"Name: {applicant.full_name}\n"
                        f"Phone: {applicant.phone_number}\n"
                        f"ID: {applicant.id_number}\n"
                        f"County: {applicant.county}\n"
                        f"Voter: {status_text}\n"
                        f"Channel: {applicant.registration_channel}\n"
                        f"Date: {applicant.registered_at.strftime('%Y-%m-%d %H:%M')}"
                    )
                except Applicant.DoesNotExist:
                    response = "END No registration found with that ID number."
                except Exception as e:
                    print(f"Status error: {e}")
                    response = "END An error occurred. Please try again."
            else:
                response = "END Invalid input. Restart."
            return HttpResponse(response, content_type="text/plain")

        elif choice == "0":
            cache.delete(cache_key)
            response = "END Thank you. Goodbye!"
            return HttpResponse(response, content_type="text/plain")

        else:
            response = "END Invalid option. Please dial again."
            return HttpResponse(response, content_type="text/plain")

    except Exception as e:
        print(f"UNEXPECTED USSD ERROR: {e}")
        return HttpResponse("END An unexpected error occurred. Please try again later.", content_type="text/plain")