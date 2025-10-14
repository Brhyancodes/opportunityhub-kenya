from django.urls import path
from .views import (
    YouthProfileView,
    SkillListCreateView,
    YouthSkillListView,
    YouthSkillAddView,
    YouthSkillDetailView,
    ExperienceListCreateView,
    ExperienceDetailView,
)

urlpatterns = [
    # Youth Profile
    path("profile/", YouthProfileView.as_view(), name="youth-profile"),
    # Skills Management
    path("skills/all/", SkillListCreateView.as_view(), name="skill-list-create"),
    path("skills/", YouthSkillListView.as_view(), name="youth-skill-list"),
    path("skills/add/", YouthSkillAddView.as_view(), name="youth-skill-add"),
    path("skills/<int:pk>/", YouthSkillDetailView.as_view(), name="youth-skill-detail"),
    # Experience Management
    path(
        "experience/", ExperienceListCreateView.as_view(), name="experience-list-create"
    ),
    path(
        "experience/<int:pk>/", ExperienceDetailView.as_view(), name="experience-detail"
    ),
]
