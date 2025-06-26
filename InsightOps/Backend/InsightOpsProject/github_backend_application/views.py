

 
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .mongo_models import Organization, User, Project, Repository, Team
from django.http import HttpResponseBadRequest
from .mongo_models import Organization, User, Team, Repository, Project
from datetime import datetime
from django import forms
import mongoengine
 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .mongo_models import Organization
from .serializers.Organization_Serializer import OrganizationSerializer
 
class OrganizationDetailView(APIView):
    def get(self, request, org_name):
        try:
            organization = Organization.objects.get(name=org_name)
            serializer = OrganizationSerializer(organization)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
class OrganizationMetricsView(APIView):
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
 
        # Validate date format
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
            end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
 
        # Validate date range
        if start_date and end_date and start_date > end_date:
            return Response({"error": "Start date must be before end date."}, status=status.HTTP_400_BAD_REQUEST)
 
        try:
            # Query all collections in the date range
            org_count = Organization.objects(
                fetched_at__gte=start_date,
                fetched_at__lte=end_date
            ).count() if start_date and end_date else Organization.objects.count()
           
            user_count = User.objects(
                fetched_at__gte=start_date,
                fetched_at__lte=end_date
            ).count() if start_date and end_date else User.objects.count()
           
            team_count = Team.objects(
                fetched_at__gte=start_date,
                fetched_at__lte=end_date
            ).count() if start_date and end_date else Team.objects.count()
           
            repo_count = Repository.objects(
                fetched_at__gte=start_date,
                fetched_at__lte=end_date
            ).count() if start_date and end_date else Repository.objects.count()
           
            project_count = Project.objects(
                fetched_at__gte=start_date,
                fetched_at__lte=end_date
            ).count() if start_date and end_date else Project.objects.count()
 
            metrics = {
                'org_count': org_count,
                'user_count': user_count,
                'team_count': team_count,
                'repo_count': repo_count,
                'project_count': project_count,
                'start_date': start_date,
                'end_date': end_date
            }
            return Response(metrics, status=status.HTTP_200_OK)
        except mongoengine.errors.MongoEngineException as e:
            return Response({"error": f"Database error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 