from django.urls import path
from .views import EmployerProfileView

urlpatterns = [
    path("profile/", EmployerProfileView.as_view(), name="employer-profile"),
]
