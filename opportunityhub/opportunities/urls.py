from django.urls import path
from .views import OpportunityListCreateView, OpportunityDetailView

urlpatterns = [
    path("", OpportunityListCreateView.as_view(), name="opportunity-list-create"),
    path("<int:pk>/", OpportunityDetailView.as_view(), name="opportunity-detail"),
]
