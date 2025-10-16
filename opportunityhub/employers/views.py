from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import EmployerProfile
from .serializers import EmployerProfileSerializer, EmployerProfileCreateSerializer


class EmployerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current employer's profile"""
        try:
            profile = EmployerProfile.objects.select_related("user").get(
                user=request.user
            )
            serializer = EmployerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmployerProfile.DoesNotExist:
            return Response(
                {"error": "Employer profile not found. Please create one."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request):
        """Update employer profile"""
        try:
            profile = EmployerProfile.objects.get(user=request.user)
            serializer = EmployerProfileCreateSerializer(
                profile, data=request.data, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                # Return full profile data
                full_serializer = EmployerProfileSerializer(profile)
                return Response(
                    {
                        "message": "Profile updated successfully",
                        "profile": full_serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployerProfile.DoesNotExist:
            return Response(
                {"error": "Employer profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
