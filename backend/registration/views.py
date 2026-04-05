# registration/views.py

import json
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from .models import Applicant, RegistrationChannel
from .serializers import ApplicantSerializer
from twilio.twiml.messaging_response import MessagingResponse
from .models import Applicant, RegistrationChannel
from django.core.cache import cache
from twilio.rest import Client

logger = logging.getLogger(__name__)

# Simple root view (optional)
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

# API Views
class ApplicantListCreateView(generics.ListCreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

class WebsiteRegistrationView(generics.CreateAPIView):
    serializer_class = ApplicantSerializer
    def perform_create(self, serializer):
        serializer.save(registration_channel=RegistrationChannel.WEBSITE)

class WhatsAppRegistrationView(generics.CreateAPIView):
    serializer_class = ApplicantSerializer
    def perform_create(self, serializer):
        serializer.save(registration_channel=RegistrationChannel.WHATSAPP)

class USSDSimulationView(APIView):
    def post(self, request):
        serializer = ApplicantSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(registration_channel=RegistrationChannel.USSD)
                return Response({"message": "Registration successful", "data": serializer.data}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "Phone number or ID already registered"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Africa's Talking USSD Callback

@csrf_exempt
@require_http_methods(["POST"])
def africastalking_ussd_callback(request):
    try:
        session_id = request.POST.get("sessionId")
        phone_number = request.POST.get("phoneNumber", "").strip()
        text = request.POST.get("text", "")

        # Normalize phone
        if phone_number and not phone_number.startswith('+'):
            phone_number = '+' + phone_number

        # Get or create session data from cache
        cache_key = f"ussd_{session_id}"
        session_data = cache.get(cache_key, {})
        
        print(f"USSD: session={session_id}, phone={phone_number}, text='{text}', data={session_data}")

        # Main menu
        if text == "":
            # Clear any previous session data
            cache.delete(cache_key)
            response = "CON Welcome to Voter Registration\n1. Register To Vote\n2. Check Voter Status\n0. Exit"
            return HttpResponse(response, content_type="text/plain")

        parts = text.split('*')
        level = len(parts)
        choice = parts[0]

        # Registration flow
        if choice == "1":
            if level == 1:
                session_data = {'step': 'name'}
                cache.set(cache_key, session_data, timeout=300)  # 5 minutes
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
                response = "CON Are you registered to vote?\n1. Yes\n2. No"
            elif level == 5:
                voter_choice = parts[4].strip()
                voter_status = (voter_choice == "1")
                name = session_data.get('name', '')
                id_num = session_data.get('id_number', '')
                county = session_data.get('county', '')
                
                if not name or not id_num or not county:
                    response = "END Registration failed: missing data. Please restart."
                else:
                    # Check duplicates
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
                # Clear session
                cache.delete(cache_key)
            else:
                response = "END Too many steps. Restart."
            return HttpResponse(response, content_type="text/plain")

        # Check status flow
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

        # Exit
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


@csrf_exempt
@require_http_methods(["POST"])
def whatsapp_webhook(request: HttpRequest):
    """
    Handles incoming WhatsApp messages from Twilio.
    """
    # Parse the incoming message from the POST request
    incoming_msg = request.POST.get('Body', '').strip()
    sender = request.POST.get('From', '').strip()

    # Use cache to store user conversation state
    cache_key = f"whatsapp_state_{sender}"
    session_data = cache.get(cache_key, {})

    # Create a TwiML response object
    resp = MessagingResponse()
    msg = resp.message()

    # Default response if the incoming message is empty or invalid
    response_text = "Sorry, I didn't understand that. Please type 'MENU' to see available options."

    # Main menu logic
    if incoming_msg.lower() == 'menu':
        response_text = (
            "🤖 *Voter Registration Bot*\n\n"
            "Choose an option:\n"
            "1️⃣ *Register* - Register to vote\n"
            "2️⃣ *Status* - Check your registration status\n"
            "0️⃣ *Exit* - End this session"
        )
        # Reset session data when user requests menu
        session_data = {}
        cache.set(cache_key, session_data, timeout=600)

    elif incoming_msg.lower() == 'exit' or (session_data.get('step') and incoming_msg.lower() == '0'):
        response_text = "Thank you for using the Voter Registration Bot. Goodbye! 👋\n\nType 'MENU' to start over."
        cache.delete(cache_key)

    elif incoming_msg == '1' or session_data.get('step') == 'awaiting_name':
        # Step 1: Capture Full Name
        if 'step' not in session_data:
            session_data['step'] = 'awaiting_name'
            cache.set(cache_key, session_data, timeout=600)
            response_text = "Please enter your *full name* as it appears on your ID:"
        else:
            session_data['full_name'] = incoming_msg
            session_data['step'] = 'awaiting_id'
            cache.set(cache_key, session_data, timeout=600)
            response_text = "Please enter your *ID Number*:"

    elif session_data.get('step') == 'awaiting_id':
        # Step 2: Capture ID Number
        session_data['id_number'] = incoming_msg
        session_data['step'] = 'awaiting_county'
        cache.set(cache_key, session_data, timeout=600)
        response_text = "Please enter your *county* of residence:"

    elif session_data.get('step') == 'awaiting_county':
        # Step 3: Capture County
        session_data['county'] = incoming_msg
        session_data['step'] = 'awaiting_voter_status'
        cache.set(cache_key, session_data, timeout=600)
        response_text = "Are you registered to vote? Reply with '1' for Yes or '2' for No:"

    elif session_data.get('step') == 'awaiting_voter_status':
        # Step 4: Process voter status and save to database
        if incoming_msg not in ['1', '2']:
            response_text = "Invalid choice. Please reply with '1' for Yes or '2' for No:"
        else:
            voter_status = incoming_msg == '1'
            try:
                # Check for duplicates
                if Applicant.objects.filter(phone_number=sender).exists():
                    response_text = "❌ This phone number is already registered."
                elif Applicant.objects.filter(id_number=session_data['id_number']).exists():
                    response_text = "❌ This ID number is already registered."
                else:
                    # Create new applicant
                    Applicant.objects.create(
                        full_name=session_data['full_name'],
                        phone_number=sender,
                        id_number=session_data['id_number'],
                        county=session_data['county'],
                        voter_status=voter_status,
                        registration_channel=RegistrationChannel.WHATSAPP
                    )
                    response_text = f"✅ Registration successful! Welcome {session_data['full_name']}.\n\nType 'MENU' for other options."
            except Exception as e:
                response_text = "❌ An internal error occurred. Please try again later."
            finally:
                # Clean up session data
                cache.delete(cache_key)

    elif incoming_msg == '2' or session_data.get('step') == 'awaiting_status_id':
        # Check registration status flow
        if 'step' not in session_data:
            session_data['step'] = 'awaiting_status_id'
            cache.set(cache_key, session_data, timeout=600)
            response_text = "Please enter your *ID Number* to check your status:"
        else:
            id_num = incoming_msg
            try:
                applicant = Applicant.objects.get(id_number=id_num)
                status_text = "registered" if applicant.voter_status else "not registered"
                response_text = (
                    f"📋 *Registration Details*\n\n"
                    f"*Name:* {applicant.full_name}\n"
                    f"*Phone:* {applicant.phone_number}\n"
                    f"*ID:* {applicant.id_number}\n"
                    f"*County:* {applicant.county}\n"
                    f"*Voter Status:* {status_text}\n"
                    f"*Channel:* {applicant.registration_channel}\n"
                    f"*Date:* {applicant.registered_at.strftime('%Y-%m-%d %H:%M')}\n\n"
                    "Type 'MENU' for other options."
                )
            except Applicant.DoesNotExist:
                response_text = "❌ No registration found with that ID number."
            except Exception as e:
                response_text = "❌ An error occurred. Please try again."
            finally:
                cache.delete(cache_key)

    else:
        # Fallback for unrecognized commands
        response_text = "Welcome to the Voter Registration Bot! 🇰🇪\n\nType *MENU* to see available options."

    # Add the response text to the TwiML message
    msg.body(response_text)
    return HttpResponse(str(resp), content_type='text/xml')

def send_whatsapp_message(to_number, message_body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message_body,
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=f'whatsapp:{to_number}'
    )
    return message.sid