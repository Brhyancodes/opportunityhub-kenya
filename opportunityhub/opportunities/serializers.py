from rest_framework import serializers
from .models import Opportunity, Skill
from employers.serializers import EmployerProfileSerializer


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
