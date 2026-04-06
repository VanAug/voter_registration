# registration/views/api_views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError
from ..models import Applicant, RegistrationChannel
from ..serializers import ApplicantSerializer

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