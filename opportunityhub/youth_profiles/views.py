from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import YouthProfile, Skill, YouthSkill, Experience
from .serializers import (
    YouthProfileSerializer,
    YouthProfileCreateSerializer,
    SkillSerializer,
    YouthSkillSerializer,
    ExperienceSerializer,
)


class YouthProfileView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT /api/youth/profile/
    View and update youth profile
    """

    serializer_class = YouthProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        youth_profile, created = YouthProfile.objects.get_or_create(
            user=self.request.user
        )
        return youth_profile

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = YouthProfileCreateSerializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return full profile with nested data
        full_serializer = YouthProfileSerializer(instance)
        return Response(full_serializer.data)


class SkillListCreateView(generics.ListCreateAPIView):
    """
    GET/POST /api/youth/skills/all/
    List all available skills or create new skill
    """

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]


class YouthSkillListView(generics.ListAPIView):
    """
    GET /api/youth/skills/
    List youth's skills
    """

    serializer_class = YouthSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        youth_profile = get_object_or_404(YouthProfile, user=self.request.user)
        return YouthSkill.objects.filter(youth_profile=youth_profile)


class YouthSkillAddView(APIView):
    """
    POST /api/youth/skills/add/
    Add a skill to youth profile
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        youth_profile, created = YouthProfile.objects.get_or_create(user=request.user)

        serializer = YouthSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(youth_profile=youth_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YouthSkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/DELETE /api/youth/skills/<id>/
    View, update, or delete a specific skill
    """

    serializer_class = YouthSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        youth_profile = get_object_or_404(YouthProfile, user=self.request.user)
        return YouthSkill.objects.filter(youth_profile=youth_profile)


class ExperienceListCreateView(generics.ListCreateAPIView):
    """
    GET/POST /api/youth/experience/
    List or create work experiences
    """

    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        youth_profile = get_object_or_404(YouthProfile, user=self.request.user)
        return Experience.objects.filter(youth_profile=youth_profile)

    def perform_create(self, serializer):
        youth_profile, created = YouthProfile.objects.get_or_create(
            user=self.request.user
        )
        serializer.save(youth_profile=youth_profile)


class ExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/DELETE /api/youth/experience/<id>/
    View, update, or delete specific experience
    """

    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        youth_profile = get_object_or_404(YouthProfile, user=self.request.user)
        return Experience.objects.filter(youth_profile=youth_profile)
