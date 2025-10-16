from django.urls import path
from .views import (
    OpportunityListCreateView,
    OpportunityDetailView,
    ApplyOpportunityView,
    MyApplicationsView,
    EmployerApplicationsView,
    ApplicationDetailView,
)

urlpatterns = [
    # Opportunities
    path("", OpportunityListCreateView.as_view(), name="opportunity-list-create"),
    path("<int:pk>/", OpportunityDetailView.as_view(), name="opportunity-detail"),
    # Applications
    path("<int:pk>/apply/", ApplyOpportunityView.as_view(), name="apply-opportunity"),
    path("applications/my/", MyApplicationsView.as_view(), name="my-applications"),
    path(
        "applications/employer/",
        EmployerApplicationsView.as_view(),
        name="employer-applications",
    ),
    path(
        "applications/<int:pk>/",
        ApplicationDetailView.as_view(),
        name="application-detail",
    ),
]
