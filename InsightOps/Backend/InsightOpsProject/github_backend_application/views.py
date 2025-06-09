

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

def organization_detail(request):
    org = Organization.objects.get(name='DevOpsRealPage')
    projects = org.projects.all()
    users = org.users.all()
    return render(request, 'Templates/organization_detail.html', {
        'organization': org,
        'projects': projects,
        'users': users
    })

def members(request):
    return HttpResponse("Hello world!")

# myapp/views.py


def create_organization(request):
    org = Organization(
        name="Test Org",
        total_repositories=0,
        total_projects=0,
        active_users_count=0
    ).save()

    user = User(
        organization=org,
        username="testuser",
        email="test@example.com"
    ).save()

    project = Project(
        organization=org,
        name="Test Project",
        number=1
    ).save()

    repository = Repository(
        organization=org,
        project=project,
        name="Test Repo",
        url="https://github.com/test/repo"
    ).save()

    team = Team(
        organization=org,
        project=project,
        name="Test Team",
        users=[user]
    ).save()

    return JsonResponse({
        "organization": str(org),
        "user": str(user),
        "project": str(project),
        "repository": str(repository),
        "team": str(team),
    })