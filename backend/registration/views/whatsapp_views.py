# registration/views/whatsapp_views.py
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from twilio.twiml.messaging_response import MessagingResponse
from ..models import Applicant, RegistrationChannel

@csrf_exempt
@require_http_methods(["POST"])
def whatsapp_webhook(request: HttpRequest):
    incoming_msg = request.POST.get('Body', '').strip()
    sender = request.POST.get('From', '').strip()

    cache_key = f"whatsapp_state_{sender}"
    session_data = cache.get(cache_key, {})

    resp = MessagingResponse()
    msg = resp.message()
    response_text = "Sorry, I didn't understand that. Please type 'MENU' to see available options."

    if incoming_msg.lower() == 'menu':
        response_text = (
            "*Voter Registration Bot*\n\n"
            "Choose an option:\n"
            "1. Register - Register to vote\n"
            "2. Status - Check your registration status\n"
            "0. Exit - End this session"
        )
        session_data = {}
        cache.set(cache_key, session_data, timeout=600)

    elif incoming_msg.lower() == 'exit' or (session_data.get('step') and incoming_msg.lower() == '0'):
        response_text = "Thank you for using the Voter Registration Bot. Goodbye!\n\nType 'MENU' to start over."
        cache.delete(cache_key)

    elif incoming_msg == '1' or session_data.get('step') == 'awaiting_name':
        if 'step' not in session_data:
            session_data['step'] = 'awaiting_name'
            cache.set(cache_key, session_data, timeout=600)
            response_text = "Please enter your full name as it appears on your ID:"
        else:
            session_data['full_name'] = incoming_msg
            session_data['step'] = 'awaiting_id'
            cache.set(cache_key, session_data, timeout=600)
            response_text = "Please enter your ID Number:"

    elif session_data.get('step') == 'awaiting_id':
        session_data['id_number'] = incoming_msg
        session_data['step'] = 'awaiting_county'
        cache.set(cache_key, session_data, timeout=600)
        response_text = "Please enter your county of residence:"

    elif session_data.get('step') == 'awaiting_county':
        session_data['county'] = incoming_msg
        session_data['step'] = 'awaiting_voter_status'
        cache.set(cache_key, session_data, timeout=600)
        response_text = "Do you wish to register as a voter? Reply with '1' for Yes or '2' for No:"

    elif session_data.get('step') == 'awaiting_voter_status':
        if incoming_msg not in ['1', '2']:
            response_text = "Invalid choice. Please reply with '1' for Yes or '2' for No:"
        else:
            voter_status = incoming_msg == '1'
            try:
                if Applicant.objects.filter(phone_number=sender).exists():
                    response_text = "This phone number is already registered."
                elif Applicant.objects.filter(id_number=session_data['id_number']).exists():
                    response_text = "This ID number is already registered."
                else:
                    Applicant.objects.create(
                        full_name=session_data['full_name'],
                        phone_number=sender,
                        id_number=session_data['id_number'],
                        county=session_data['county'],
                        voter_status=voter_status,
                        registration_channel=RegistrationChannel.WHATSAPP
                    )
                    response_text = f"Registration successful! Welcome {session_data['full_name']}.\n\nType 'MENU' for other options."
            except Exception as e:
                response_text = "An internal error occurred. Please try again later."
            finally:
                cache.delete(cache_key)

    elif incoming_msg == '2' or session_data.get('step') == 'awaiting_status_id':
        if 'step' not in session_data:
            session_data['step'] = 'awaiting_status_id'
            cache.set(cache_key, session_data, timeout=600)
            response_text = "Please enter your ID Number to check your status:"
        else:
            id_num = incoming_msg
            try:
                applicant = Applicant.objects.get(id_number=id_num)
                status_text = "registered" if applicant.voter_status else "not registered"
                response_text = (
                    f"Registration Details\n\n"
                    f"Name: {applicant.full_name}\n"
                    f"Phone: {applicant.phone_number}\n"
                    f"ID: {applicant.id_number}\n"
                    f"County: {applicant.county}\n"
                    f"Voter Status: {status_text}\n"
                    f"Channel: {applicant.registration_channel}\n"
                    f"Date: {applicant.registered_at.strftime('%Y-%m-%d %H:%M')}\n\n"
                    "Type 'MENU' for other options."
                )
            except Applicant.DoesNotExist:
                response_text = "No registration found with that ID number."
            except Exception as e:
                response_text = "An error occurred. Please try again."
            finally:
                cache.delete(cache_key)

    else:
        response_text = "Welcome to the Voter Registration Bot!\n\nType *MENU* to see available options."

    msg.body(response_text)
    return HttpResponse(str(resp), content_type='text/xml')