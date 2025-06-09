import requests
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import os
from decouple import config
from mongoengine import connect, DoesNotExist, MultipleObjectsReturned
from  mongo_models import Organization, User, Project, Repository, Team

# Step 1: Initialize configuration and MongoDB connection
ORG_NAME = "DevOpsRealPage"
TOKEN = config('GITHUB_TOKEN', default='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')
REST_BASE_URL = "https://api.github.com"
GRAPHQL_URL = "https://api.github.com/graphql"
PER_PAGE = 10

# Connect to MongoDB Atlas
MONGO_URI = config('MONGO_URI', default='mongodb+srv://narendhar879:GopalReddy998@clusterforspringboot.dpssn.mongodb.net/InsightOpsDb?retryWrites=true&w=majority&appName=ClusterForSpringboot')
try:
    connect(db='InsightOpsDb', host=MONGO_URI)
    print("Successfully connected to MongoDB Atlas")
except Exception as e:
    print(f"Failed to connect to MongoDB Atlas: {str(e)}")
    raise

# REST API headers
REST_HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# GraphQL client setup with SSL verification
transport = AIOHTTPTransport(url=GRAPHQL_URL, headers={"Authorization": f"Bearer {TOKEN}"}, ssl=True)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Step 2: Define function to fetch repositories using REST API
def fetch_repositories():
    """Fetch all repositories using REST API."""
    repos_url = f"{REST_BASE_URL}/orgs/{ORG_NAME}/repos"
    repos = []
    page = 1
    while True:
        paginated_url = f"{repos_url}?per_page={PER_PAGE}&page={page}"
        response = requests.get(paginated_url, headers=REST_HEADERS)
        if response.status_code != 200:
            print(f"Error fetching repositories: {response.status_code} - {response.json()}")
            return repos
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
        if 'Link' not in response.headers or 'rel="next"' not in response.headers['Link']:
            break
    return repos

# Step 3: Define function to fetch organization members using REST API
def fetch_members():
    """Fetch all organization members using REST API."""
    members_url = f"{REST_BASE_URL}/orgs/{ORG_NAME}/members"
    members = []
    page = 1
    while True:
        paginated_url = f"{members_url}?per_page={PER_PAGE}&page={page}"
        response = requests.get(paginated_url, headers=REST_HEADERS)
        if response.status_code != 200:
            print(f"Error fetching members: {response.status_code} - {response.json()}")
            return members
        data = response.json()
        if not data:
            break
        members.extend(data)
        page += 1
        if 'Link' not in response.headers or 'rel="next"' not in response.headers['Link']:
            break
    return members

# Step 4: Define function to fetch user email using REST API
def fetch_user_email(username):
    """Fetch user email using REST API."""
    user_url = f"{REST_BASE_URL}/users/{username}"
    response = requests.get(user_url, headers=REST_HEADERS)
    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('email', None)
    else:
        print(f"Error fetching user {username}: {response.status_code}")
        return None

# Step 5: Define function to fetch Projects V2 using GraphQL API
def fetch_v2_projects():
    """Fetch Projects V2 using GraphQL API."""
    query = gql("""
    query($org: String!, $first: Int, $after: String) {
      organization(login: $org) {
        projectsV2(first: $first, after: $after) {
          totalCount
          nodes {
            id
            title
            number
            teams(first: 10) {
              nodes {
                name
                members(first: 10) {
                  nodes {
                    login
                  }
                }
              }
            }
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
    """)
    projects = []
    after = None
    while True:
        params = {"org": ORG_NAME, "first": PER_PAGE, "after": after}
        try:
            result = client.execute(query, variable_values=params)
        except Exception as e:
            print(f"Error fetching Projects V2: {str(e)}")
            return []
        org = result.get("organization", {})
        projects_v2 = org.get("projectsV2", {})
        projects.extend(projects_v2.get("nodes", []))
        page_info = projects_v2.get("pageInfo", {})
        if not page_info.get("hasNextPage", False):
            break
        after = page_info.get("endCursor")
    return projects

# Step 6: Define function to fetch repositories associated with a Project V2
def fetch_project_repositories(project_id):
    """Fetch repositories associated with a Project V2 by examining its items."""
    query = gql("""
    query($projectId: ID!, $first: Int, $after: String) {
      node(id: $projectId) {
        ... on ProjectV2 {
          items(first: $first, after: $after) {
            nodes {
              content {
                ... on Issue {
                  repository {
                    name
                    url
                  }
                }
                ... on PullRequest {
                  repository {
                    name
                    url
                  }
                }
              }
            }
            pageInfo {
              hasNextPage
              endCursor
            }
          }
        }
      }
    }
    """)
    repositories = set()
    after = None
    while True:
        params = {"projectId": project_id, "first": PER_PAGE, "after": after}
        try:
            result = client.execute(query, variable_values=params)
        except Exception as e:
            print(f"Error fetching repositories for project {project_id}: {str(e)}")
            return []
        items = result.get("node", {}).get("items", {}).get("nodes", [])
        for item in items:
            if item.get("content") and item["content"].get("repository"):
                repo = item["content"]["repository"]
                repositories.add((repo["name"], repo["url"]))
        page_info = result.get("node", {}).get("items", {}).get("pageInfo", {})
        if not page_info.get("hasNextPage", False):
            break
        after = page_info.get("endCursor")
    return [{"name": name, "url": url} for name, url in repositories]

# Step 7: Main function to orchestrate data fetching and saving to MongoDB
def main():
    # Create or update Organization
    try:
        org = Organization.objects.get(name=ORG_NAME)
        created = False
        print(f"Organization {ORG_NAME} already exists, updating...")
    except DoesNotExist:
        org = Organization.objects.create(
            name=ORG_NAME,
            total_repositories=0,
            total_projects=0,
            active_users_count=0
        )
        created = True
        print(f"Created new Organization: {ORG_NAME}")
    except MultipleObjectsReturned:
        print(f"Error: Multiple organizations found with name {ORG_NAME}")
        raise
    except Exception as e:
        print(f"Error accessing Organization: {str(e)}")
        raise

    # Fetch data
    repositories = fetch_repositories()
    members = fetch_members()
    projects = fetch_v2_projects()

    # Step 8: Save Users (organization members and project team members)
    active_users = set()
    for member in members:
        active_users.add(member["login"])
    for project in projects:
        for team in project["teams"]["nodes"]:
            for member in team["members"]["nodes"]:
                active_users.add(member["login"])

    for username in active_users:
        try:
            user = User.objects.get(organization=org, username=username)
        except DoesNotExist:
            email = fetch_user_email(username)
            user = User.objects.create(
                organization=org,
                username=username,
                email=email
            )
        except MultipleObjectsReturned:
            print(f"Error: Multiple users found with username {username}")
            raise

    # Step 9: Save Projects and associated data
    for project_data in projects:
        try:
            project = Project.objects.get(organization=org, number=project_data["number"])
        except DoesNotExist:
            project = Project.objects.create(
                organization=org,
                number=project_data["number"],
                name=project_data["title"]
            )
        except MultipleObjectsReturned:
            print(f"Error: Multiple projects found with number {project_data['number']} for organization {ORG_NAME}")
            raise

        # Save Repositories for this project
        project_repos = fetch_project_repositories(project_data["id"])
        for repo_data in project_repos:
            try:
                Repository.objects.get(organization=org, project=project, name=repo_data["name"])
            except DoesNotExist:
                Repository.objects.create(
                    organization=org,
                    project=project,
                    name=repo_data["name"],
                    url=repo_data["url"]
                )
            except MultipleObjectsReturned:
                print(f"Error: Multiple repositories found with name {repo_data['name']} for project {project.name}")
                raise

        # Save Teams and their members
        for team_data in project_data["teams"]["nodes"]:
            try:
                team = Team.objects.get(organization=org, project=project, name=team_data["name"])
            except DoesNotExist:
                team = Team.objects.create(
                    organization=org,
                    project=project,
                    name=team_data["name"]
                )
            except MultipleObjectsReturned:
                print(f"Error: Multiple teams found with name {team_data['name']} for project {project.name}")
                raise

            # Update team members
            team_users = []
            for member in team_data["members"]["nodes"]:
                user = User.objects(organization=org, username=member["login"]).first()
                if user:
                    team_users.append(user)
            team.users = team_users
            team.save()

    # Step 10: Update Organization counts
    org.total_repositories = len(repositories)
    org.total_projects = len(projects)
    org.active_users_count = len(active_users)
    org.save()

    # Step 11: Print summary
    print(f"Organization: {org.name}")
    print(f"Total Repositories: {org.total_repositories}")
    print(f"Total Projects: {org.total_projects}")
    print(f"Active Users: {org.active_users_count}")
    print("\nProjects:")
    for project in Project.objects(organization=org):
        print(f"\nProject: {project.name} (Number: {project.number})")
        repos = Repository.objects(project=project)
        print(f"Repositories: {len(repos)}")
        for repo in repos:
            print(f"  - {repo.name} ({repo.url})")
        teams = Team.objects(project=project)
        print(f"Teams: {len(teams)}")
        for team in teams:
            print(f"  - {team.name}: {', '.join(str(user) for user in team.users)}")
    print("\nActive Users:")
    for user in User.objects(organization=org):
        print(f"  Username: {user.username}, Email: {user.email or 'Not available'}")

if __name__ == "__main__":
    main()