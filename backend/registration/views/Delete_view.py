from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from ..models import Applicant
from ..serializers import ApplicantSerializer


class ApplicantDeleteView(generics.DestroyAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"message": "Applicant deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)