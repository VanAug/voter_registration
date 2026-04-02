from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError
from .models import Applicant, RegistrationChannel
from .serializers import ApplicantSerializer
from django.http import JsonResponse

# Generic list/create view for all applicants (admin use)
class ApplicantListCreateView(generics.ListCreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

# Endpoint for website registration (channel forced to WEBSITE)
class WebsiteRegistrationView(generics.CreateAPIView):
    serializer_class = ApplicantSerializer

    def perform_create(self, serializer):
        serializer.save(registration_channel=RegistrationChannel.WEBSITE)

# Endpoint for WhatsApp registration (channel forced to WHATSAPP)
class WhatsAppRegistrationView(generics.CreateAPIView):
    serializer_class = ApplicantSerializer

    def perform_create(self, serializer):
        serializer.save(registration_channel=RegistrationChannel.WHATSAPP)

# Endpoint for USSD registration (channel forced to USSD)
class USSDSimulationView(APIView):
    """
    Simulates USSD registration flow.
    Expects a POST with: { "phone_number": "...", "full_name": "...", "id_number": "...", "county": "...", "voter_status": true/false }
    In real USSD, you'd handle step-by-step sessions. This is a simplified one-shot.
    """
    def post(self, request):
        serializer = ApplicantSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(registration_channel=RegistrationChannel.USSD)
                return Response({"message": "Registration successful", "data": serializer.data}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "Phone number or ID already registered"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Optional: Africa's Talking USSD webhook (stateful)
class AfricaTalkingUSSDRedirect(APIView):
    """
    Handle Africa's Talking USSD callback.
    Expects: POST with sessionId, phoneNumber, text, networkCode, serviceCode
    Returns plain text response for USSD.
    """
    def post(self, request):
        # Get USSD input
        session_id = request.POST.get('sessionId')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text', '')  # user input, * separated steps

        # Simple state machine
        if text == '':
            response = "CON Welcome to Voter Registration\n1. Register\n0. Exit"
        elif text == '1':
            response = "CON Enter your full name:"
        elif text.startswith('1*'):
            parts = text.split('*')
            if len(parts) == 2:
                # Store name in session (you'd use a cache or DB session)
                request.session['full_name'] = parts[1]
                response = "CON Enter your ID number:"
            elif len(parts) == 3:
                request.session['id_number'] = parts[2]
                response = "CON Enter your county:"
            elif len(parts) == 4:
                request.session['county'] = parts[3]
                response = "CON Are you registered to vote?\n1. Yes\n2. No"
            elif len(parts) == 5:
                voter_status = parts[4] == '1'
                # Save to DB
                try:
                    Applicant.objects.create(
                        full_name=request.session.get('full_name'),
                        phone_number=phone_number,
                        id_number=request.session.get('id_number'),
                        county=request.session.get('county'),
                        voter_status=voter_status,
                        registration_channel=RegistrationChannel.USSD
                    )
                    response = "END Registration successful! Thank you."
                    # Clear session
                    request.session.flush()
                except IntegrityError:
                    response = "END Phone number or ID already registered."
            else:
                response = "END Invalid input. Please try again."
        else:
            response = "END Invalid option."

        return Response(response, content_type='text/plain')
    
def root_view(request):
    return JsonResponse({
        "message": "Welcome to Voter Registration API",
        "endpoints": {
            "admin": "/admin/",
            "api_applicants": "/api/applicants/",
            "web_registration": "/api/register/web/",
            "whatsapp_registration": "/api/register/whatsapp/",
            "ussd_simulation": "/api/register/ussd/simulate/"
        }
    })