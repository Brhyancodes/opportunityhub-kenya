from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Opportunity
from employers.models import EmployerProfile
from .serializers import OpportunitySerializer, OpportunityCreateUpdateSerializer


class OpportunityListCreateView(APIView):
    """
    GET: List all opportunities (with filtering)
    POST: Create new opportunity (employers only)
    """

    def get_permissions(self):
        # Anyone can view opportunities, only authenticated users can create
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        """List opportunities with optional filtering"""
        opportunities = (
            Opportunity.objects.select_related("employer", "employer__user")
            .prefetch_related("required_skills")
            .filter(is_active=True)
        )

        # Filter by category
        category = request.query_params.get("category")
        if category:
            opportunities = opportunities.filter(category__iexact=category)

        # Filter by county/location
        county = request.query_params.get("county")
        if county:
            opportunities = opportunities.filter(county__iexact=county)

        # Filter by skill
        skill = request.query_params.get("skill")
        if skill:
            opportunities = opportunities.filter(required_skills__name__iexact=skill)

        # Filter by opportunity type
        opp_type = request.query_params.get("type")
        if opp_type:
            opportunities = opportunities.filter(opportunity_type__iexact=opp_type)

        serializer = OpportunitySerializer(opportunities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create new opportunity (employers only)"""
        # Check if user has employer profile
        try:
            employer_profile = EmployerProfile.objects.get(user=request.user)
        except EmployerProfile.DoesNotExist:
            return Response(
                {"error": "Only employers can create opportunities"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = OpportunityCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            opportunity = serializer.save(employer=employer_profile)
            # Return full opportunity data
            full_serializer = OpportunitySerializer(opportunity)
            return Response(
                {
                    "message": "Opportunity created successfully",
                    "opportunity": full_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OpportunityDetailView(APIView):
    """
    GET: Retrieve single opportunity
    PUT: Update opportunity (employer owner only)
    DELETE: Delete opportunity (employer owner only)
    """

    def get_permissions(self):
        # Anyone can view, only authenticated can modify
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        """Get single opportunity details"""
        opportunity = get_object_or_404(
            Opportunity.objects.select_related(
                "employer", "employer__user"
            ).prefetch_related("required_skills"),
            pk=pk,
        )
        serializer = OpportunitySerializer(opportunity)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update opportunity (owner only)"""
        opportunity = get_object_or_404(Opportunity, pk=pk)

        # Check if user is the owner
        try:
            employer_profile = EmployerProfile.objects.get(user=request.user)
            if opportunity.employer != employer_profile:
                return Response(
                    {"error": "You can only update your own opportunities"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except EmployerProfile.DoesNotExist:
            return Response(
                {"error": "Employer profile not found"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = OpportunityCreateUpdateSerializer(
            opportunity, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            # Return full opportunity data
            full_serializer = OpportunitySerializer(opportunity)
            return Response(
                {
                    "message": "Opportunity updated successfully",
                    "opportunity": full_serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete opportunity (owner only)"""
        opportunity = get_object_or_404(Opportunity, pk=pk)

        # Check if user is the owner
        try:
            employer_profile = EmployerProfile.objects.get(user=request.user)
            if opportunity.employer != employer_profile:
                return Response(
                    {"error": "You can only delete your own opportunities"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except EmployerProfile.DoesNotExist:
            return Response(
                {"error": "Employer profile not found"},
                status=status.HTTP_403_FORBIDDEN,
            )

        opportunity.delete()
        return Response(
            {"message": "Opportunity deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


from .models import Application
from .serializers import (
    ApplicationSerializer,
    ApplicationCreateSerializer,
    ApplicationStatusUpdateSerializer,
)


class ApplyOpportunityView(APIView):
    """
    POST: Youth applies for an opportunity
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Apply for an opportunity"""
        # Check if user is youth
        if request.user.user_type != "youth":
            return Response(
                {"error": "Only youth users can apply for opportunities"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get the opportunity
        opportunity = get_object_or_404(Opportunity, pk=pk, is_active=True)

        # Check if already applied
        if Application.objects.filter(
            opportunity=opportunity, youth=request.user
        ).exists():
            return Response(
                {"error": "You have already applied for this opportunity"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate and create application
        serializer = ApplicationCreateSerializer(
            data=request.data, context={"opportunity": opportunity}
        )

        if serializer.is_valid():
            application = serializer.save(opportunity=opportunity, youth=request.user)
            # Return full application data
            full_serializer = ApplicationSerializer(application)
            return Response(
                {
                    "message": "Application submitted successfully",
                    "application": full_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyApplicationsView(APIView):
    """
    GET: Youth views their own applications
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List current user's applications"""
        if request.user.user_type != "youth":
            return Response(
                {"error": "Only youth users can view applications"},
                status=status.HTTP_403_FORBIDDEN,
            )

        applications = (
            Application.objects.select_related(
                "opportunity", "opportunity__employer", "opportunity__employer__user"
            )
            .prefetch_related("opportunity__required_skills")
            .filter(youth=request.user)
        )

        # Filter by status if provided
        status_filter = request.query_params.get("status")
        if status_filter:
            applications = applications.filter(status=status_filter)

        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployerApplicationsView(APIView):
    """
    GET: Employers view applications for their opportunities
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List applications for employer's opportunities"""
        # Check if user is employer
        try:
            employer_profile = EmployerProfile.objects.get(user=request.user)
        except EmployerProfile.DoesNotExist:
            return Response(
                {"error": "Only employers can view applications"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get all applications for this employer's opportunities
        applications = Application.objects.select_related(
            "youth", "opportunity"
        ).filter(opportunity__employer=employer_profile)

        # Filter by opportunity if provided
        opportunity_id = request.query_params.get("opportunity")
        if opportunity_id:
            applications = applications.filter(opportunity_id=opportunity_id)

        # Filter by status if provided
        status_filter = request.query_params.get("status")
        if status_filter:
            applications = applications.filter(status=status_filter)

        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApplicationDetailView(APIView):
    """
    GET: View single application
    PUT: Update application status (employer only)
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get application details"""
        application = get_object_or_404(
            Application.objects.select_related(
                "youth", "opportunity", "opportunity__employer"
            ),
            pk=pk,
        )

        # Check if user has permission to view
        if request.user.user_type == "youth":
            if application.youth != request.user:
                return Response(
                    {"error": "You can only view your own applications"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            # Check if employer owns the opportunity
            try:
                employer_profile = EmployerProfile.objects.get(user=request.user)
                if application.opportunity.employer != employer_profile:
                    return Response(
                        {
                            "error": "You can only view applications for your opportunities"
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )
            except EmployerProfile.DoesNotExist:
                return Response(
                    {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
                )

        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update application status (employer only)"""
        application = get_object_or_404(Application, pk=pk)

        # Check if user is employer and owns the opportunity
        try:
            employer_profile = EmployerProfile.objects.get(user=request.user)
            if application.opportunity.employer != employer_profile:
                return Response(
                    {
                        "error": "You can only update applications for your opportunities"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        except EmployerProfile.DoesNotExist:
            return Response(
                {"error": "Only employers can update application status"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ApplicationStatusUpdateSerializer(
            application, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            # Return full application data
            full_serializer = ApplicationSerializer(application)
            return Response(
                {
                    "message": "Application status updated successfully",
                    "application": full_serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
