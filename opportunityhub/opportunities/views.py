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
