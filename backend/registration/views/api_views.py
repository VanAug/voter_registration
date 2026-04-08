from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError

from ..models import Applicant, RegistrationChannel
from ..serializers import ApplicantSerializer


class ApplicantListCreateView(generics.ListCreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]


class WebsiteRegistrationView(generics.CreateAPIView):
    serializer_class = ApplicantSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(registration_channel=RegistrationChannel.WEBSITE)


class WhatsAppRegistrationView(generics.CreateAPIView):
    serializer_class = ApplicantSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(registration_channel=RegistrationChannel.WHATSAPP)


class USSDSimulationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ApplicantSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(registration_channel=RegistrationChannel.USSD)
                return Response(
                    {"message": "Registration successful", "data": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:
                return Response(
                    {"error": "Phone number or ID already registered"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "")

        if not username or not password:
            return Response(
                {"detail": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_staff:
            return Response(
                {"detail": "You are not authorized to access the admin dashboard."},
                status=status.HTTP_403_FORBIDDEN,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": user.username,
            },
            status=status.HTTP_200_OK,
        )