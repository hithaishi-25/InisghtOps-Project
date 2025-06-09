# myapp/mongo_models.py
from mongoengine import (
    Document,
    StringField,
    IntField,
    EmailField,
    ReferenceField,
    ListField,
    CASCADE,
)

class Organization(Document):
    name = StringField(max_length=255, unique=True, required=True)
    total_repositories = IntField(default=0, min_value=0)
    total_projects = IntField(default=0, min_value=0)
    active_users_count = IntField(default=0, min_value=0)

    def __str__(self):
        return self.name

    meta = {
        'collection': 'organizations',  # Matches Django's db_table
        'indexes': ['name'],  # Ensure unique index on name
    }

class User(Document):
    organization = ReferenceField(Organization, reverse_delete_rule=CASCADE, required=True)
    username = StringField(max_length=255, unique=True, required=True)
    email = EmailField(max_length=255, null=True)

    def __str__(self):
        return self.username

    meta = {
        'collection': 'users',  # Matches Django's db_table
        'indexes': ['username'],  # Ensure unique index on username
    }

class Project(Document):
    organization = ReferenceField(Organization, reverse_delete_rule=CASCADE, required=True)
    name = StringField(max_length=255, required=True)
    number = IntField(required=True)

    def __str__(self):
        return f"{self.name} (#{self.number})"

    meta = {
        'collection': 'projects',  # Matches Django's db_table
        'indexes': [
            {'fields': ['organization', 'number'], 'unique': True},  # Matches unique_together
        ],
    }

class Repository(Document):
    organization = ReferenceField(Organization, reverse_delete_rule=CASCADE, required=True)
    project = ReferenceField(Project, reverse_delete_rule=CASCADE, required=True)
    name = StringField(max_length=255, required=True)
    url = StringField(max_length=500, required=True)

    def __str__(self):
        return self.name

    meta = {
        'collection': 'repositories',  # Matches Django's db_table
    }

class Team(Document):
    organization = ReferenceField(Organization, reverse_delete_rule=CASCADE, required=True)
    project = ReferenceField(Project, reverse_delete_rule=CASCADE, required=True)
    name = StringField(max_length=255, required=True)
    users = ListField(ReferenceField(User))

    def __str__(self):
        return self.name

    meta = {
        'collection': 'teams',  # Matches Django's db_table
    }