from rest_framework import serializers
from .models import Opportunity, Skill, Application
from employers.serializers import EmployerProfileSerializer
from accounts.serializers import UserSerializer


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class OpportunitySerializer(serializers.ModelSerializer):
    """
    Full serializer for listing opportunities with all details
    """

    employer = EmployerProfileSerializer(read_only=True)
    required_skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            "id",
            "employer",
            "title",
            "description",
            "category",
            "opportunity_type",
            "county",
            "city",
            "required_skills",
            "experience_required",
            "salary_min",
            "salary_max",
            "application_deadline",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class OpportunityCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating opportunities
    """

    required_skills = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Opportunity
        fields = [
            "title",
            "description",
            "category",
            "opportunity_type",
            "county",
            "city",
            "required_skills",
            "experience_required",
            "salary_min",
            "salary_max",
            "application_deadline",
            "is_active",
        ]

    def create(self, validated_data):
        skills_data = validated_data.pop("required_skills", [])
        opportunity = Opportunity.objects.create(**validated_data)

        # Add skills
        for skill_name in skills_data:
            skill, created = Skill.objects.get_or_create(name=skill_name.strip())
            opportunity.required_skills.add(skill)

        return opportunity

    def update(self, instance, validated_data):
        skills_data = validated_data.pop("required_skills", None)

        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update skills if provided
        if skills_data is not None:
            instance.required_skills.clear()
            for skill_name in skills_data:
                skill, created = Skill.objects.get_or_create(name=skill_name.strip())
                instance.required_skills.add(skill)

        return instance


from accounts.serializers import UserSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Full serializer for viewing applications with nested data
    """

    youth = UserSerializer(read_only=True)
    opportunity = OpportunitySerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "opportunity",
            "youth",
            "status",
            "cover_letter",
            "applied_at",
            "updated_at",
        ]
        read_only_fields = ["id", "applied_at", "updated_at"]


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating applications (youth applying)
    """

    class Meta:
        model = Application
        fields = ["cover_letter"]

    def validate(self, data):
        # Check if opportunity is still active
        opportunity = self.context.get("opportunity")
        if not opportunity.is_active:
            raise serializers.ValidationError("This opportunity is no longer active")

        # Check if deadline has passed
        if opportunity.application_deadline:
            from django.utils import timezone

            if opportunity.application_deadline < timezone.now().date():
                raise serializers.ValidationError("Application deadline has passed")

        return data


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for employers to update application status
    """

    class Meta:
        model = Application
        fields = ["status"]

    def validate_status(self, value):
        if value not in ["pending", "reviewing", "accepted", "rejected"]:
            raise serializers.ValidationError("Invalid status")
        return value
