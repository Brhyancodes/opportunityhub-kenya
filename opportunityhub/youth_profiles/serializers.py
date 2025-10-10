from rest_framework import serializers
from .models import YouthProfile, Skill, YouthSkill, Experience
from accounts.serializers import UserSerializer


class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer for Skill model
    """

    class Meta:
        model = Skill
        fields = ["id", "name", "category", "created_at"]
        read_only_fields = ["id", "created_at"]


class YouthSkillSerializer(serializers.ModelSerializer):
    """
    Serializer for YouthSkill (with proficiency)
    """

    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), source="skill", write_only=True
    )

    class Meta:
        model = YouthSkill
        fields = [
            "id",
            "skill",
            "skill_id",
            "proficiency",
            "years_of_experience",
            "added_at",
        ]
        read_only_fields = ["id", "added_at"]


class ExperienceSerializer(serializers.ModelSerializer):
    """
    Serializer for work experience
    """

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "company",
            "description",
            "start_date",
            "end_date",
            "is_current",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        """
        Check that end_date is after start_date
        """
        if attrs.get("end_date") and attrs.get("start_date"):
            if attrs["end_date"] < attrs["start_date"]:
                raise serializers.ValidationError(
                    {"end_date": "End date must be after start date."}
                )
        return attrs


class YouthProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Youth Profile
    """

    user = UserSerializer(read_only=True)
    skills = YouthSkillSerializer(source="youthskill_set", many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = YouthProfile
        fields = [
            "id",
            "user",
            "age",
            "county",
            "city",
            "preferred_work_type",
            "skills",
            "education_level",
            "years_of_experience",
            "experiences",
            "profile_completed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class YouthProfileCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for creating/updating youth profile
    """

    class Meta:
        model = YouthProfile
        fields = [
            "age",
            "county",
            "city",
            "preferred_work_type",
            "education_level",
            "years_of_experience",
        ]
