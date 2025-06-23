from mongoengine import Document, ReferenceField, StringField, DateTimeField, ListField, IntField
from datetime import datetime
 
class Organization(Document):
    name = StringField(required=True, unique=True)
    total_repositories = IntField(default=0)
    total_projects = IntField(default=0)
    active_users_count = IntField(default=0)
    created_at = DateTimeField()
    fetched_at = DateTimeField()
    meta = {
        'indexes': [
            {'fields': ['fetched_at']}  # Index for date range queries
        ]
    }
 
class User(Document):
    organization = ReferenceField(Organization, required=True)
    username = StringField(required=True, unique_with='organization')
    email = StringField()
    created_at = DateTimeField()
    fetched_at = DateTimeField()
    meta = {
        'indexes': [
            {'fields': ['organization', 'username'], 'unique': True},
            {'fields': ['fetched_at']}  # Index for date range queries
        ]
    }
 
class Project(Document):
    organization = ReferenceField(Organization, required=True)
    number = IntField(required=True, unique_with='organization')
    name = StringField(required=True)
    created_at = DateTimeField()
    fetched_at = DateTimeField()
    meta = {
        'indexes': [
            {'fields': ['organization', 'number'], 'unique': True},
            {'fields': ['fetched_at']}  # Index for date range queries
        ]
    }
 
class Repository(Document):
    organization = ReferenceField(Organization, required=True)
    project = ReferenceField(Project)
    name = StringField(required=True, unique_with='organization')
    url = StringField(required=True)
    created_at = DateTimeField()
    fetched_at = DateTimeField()
    meta = {
        'indexes': [
            {'fields': ['organization', 'name'], 'unique': True},
            {'fields': ['fetched_at']}  # Index for date range queries
        ]
    }
 
class Team(Document):
    organization = ReferenceField(Organization, required=True)
    project = ReferenceField(Project, required=True)
    name = StringField(required=True, unique_with=['organization', 'project'])
    users = ListField(ReferenceField(User))
    created_at = DateTimeField()
    fetched_at = DateTimeField()
    meta = {
        'indexes': [
            {'fields': ['organization', 'project', 'name'], 'unique': True},
            {'fields': ['fetched_at']}  # Index for date range queries
        ]
    }