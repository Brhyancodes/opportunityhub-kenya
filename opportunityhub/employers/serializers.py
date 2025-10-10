from rest_framework import serializers
from .models import EmployerProfile
from accounts.serializers import UserSerializer


class EmployerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Employer Profile
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = EmployerProfile
        fields = [
            "id",
            "user",
            "company_name",
            "company_description",
            "industry",
            "company_website",
            "company_email",
            "company_phone",
            "county",
            "city",
            "address",
            "verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "verified", "created_at", "updated_at"]


class EmployerProfileCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for creating/updating employer profile
    """

    class Meta:
        model = EmployerProfile
        fields = [
            "company_name",
            "company_description",
            "industry",
            "company_website",
            "company_email",
            "company_phone",
            "county",
            "city",
            "address",
        ]
