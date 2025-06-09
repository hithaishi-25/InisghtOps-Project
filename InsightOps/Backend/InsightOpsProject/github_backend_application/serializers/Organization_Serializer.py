from rest_framework import serializers
from ..mongo_models import Organization

class OrganizationSerializer(serializers.Serializer):
    name = serializers.CharField()
    total_repositories = serializers.IntegerField()
    total_projects = serializers.IntegerField()
    active_users_count = serializers.IntegerField()

    class Meta:
        model = Organization
        fields = ['name', 'total_repositories', 'total_projects', 'active_users_count']