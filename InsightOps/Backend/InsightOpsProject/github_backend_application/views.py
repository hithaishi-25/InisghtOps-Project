

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse
from .mongo_models import Organization, User, Project, Repository, Team


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .mongo_models import Organization
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

