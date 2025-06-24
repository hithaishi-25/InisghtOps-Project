import requests
import time
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from decouple import config
from mongoengine import connect, DoesNotExist, MultipleObjectsReturned, NotUniqueError
from datetime import datetime, timezone
import logging
from mongo_models import Organization, User, Project, Repository, Team
 
# Configure logging
logging.basicConfig(
    filename='logs/github_fetch.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
# Initialize configuration and MongoDB connection
ORG_NAME = "DevOpsRealPage"
#remove this below comment to run your script smoothly
TOKEN = config('GITHUB_TOKEN', default='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')
REST_BASE_URL = "https://api.github.com"
GRAPHQL_URL = "https://api.github.com/graphql"
PER_PAGE = 100
 
# Connect to MongoDB Atlas
MONGO_URI = config('MONGO_URI', default='your-mongo-uri-here')
try:
    connect(db='InsightOpsDb', host=MONGO_URI)
    logging.info("Successfully connected to MongoDB Atlas")
    print("Successfully connected to MongoDB Atlas")
except Exception as e:
    logging.error(f"Failed to connect to MongoDB Atlas: {str(e)}")
    print(f"Error connecting to MongoDB Atlas: {str(e)}")
    raise
 
# REST API headers
REST_HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
 
# GraphQL client setup
transport = AIOHTTPTransport(url=GRAPHQL_URL, headers={"Authorization": f"Bearer {TOKEN}"}, ssl=True)
client = Client(transport=transport, fetch_schema_from_transport=True)
 
# Check rate limit for REST API
def check_rate_limit(response):
    try:
        remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        if remaining < 5:
            reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
            sleep_time = max(reset_time - int(time.time()), 0) + 5
            logging.warning(f"Rate limit low ({remaining} remaining). Sleeping for {sleep_time} seconds")
            print(f"Rate limit low. Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
    except ValueError as e:
        logging.warning(f"Error checking rate limit: {str(e)}")
 
# Fetch repositories using REST API
def fetch_repositories():
    repos_url = f"{REST_BASE_URL}/orgs/{ORG_NAME}/repos"
    repos = []
    page = 1
    while True:
        url = f"{repos_url}?per_page={PER_PAGE}&page={page}"
        response = requests.get(url, headers=REST_HEADERS)
        check_rate_limit(response)
        if response.status_code != 200:
            logging.error(f"Error fetching repositories at {url}: {response.status_code} - {response.json()}")
            print(f"Error fetching repositories: {response.status_code} - {response.json()}")
            return None
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
        if 'Link' not in response.headers or 'rel="next"' not in response.headers['Link']:
            break
    logging.info(f"Fetched {len(repos)} repositories")
    return repos
 
# Fetch organization members using REST API
def fetch_members():
    members_url = f"{REST_BASE_URL}/orgs/{ORG_NAME}/members"
    members = []
    page = 1
    while True:
        url = f"{members_url}?per_page={PER_PAGE}&page={page}"
        response = requests.get(url, headers=REST_HEADERS)
        check_rate_limit(response)
        if response.status_code != 200:
            logging.error(f"Error fetching members at {url}: {response.status_code} - {response.json()}")
            print(f"Error fetching members: {response.status_code} - {response.json()}")
            return None
        data = response.json()
        if not data:
            break
        members.extend(data)
        page += 1
        if 'Link' not in response.headers or 'rel="next"' not in response.headers['Link']:
            break
    logging.info(f"Fetched {len(members)} members")
    return members
 
# Fetch user email using REST API
def fetch_user_email(username):
    user_url = f"{REST_BASE_URL}/users/{username}"
    response = requests.get(user_url, headers=REST_HEADERS)
    check_rate_limit(response)
    if response.status_code == 200:
        user_data = response.json()
        email = user_data.get('email', None)
        logging.info(f"Fetched email for user {username}: {email}")
        return email
    else:
        logging.error(f"Error fetching user {username}: {response.status_code}")
        print(f"Error fetching user {username}: {response.status_code}")
        return None
 
# Fetch Projects V2 using GraphQL API
def fetch_v2_projects():
    query = gql("""
    query($org: String!, $first: Int, $after: String) {
      organization(login: $org) {
        createdAt
        projectsV2(first: $first, after: $after) {
          totalCount
          nodes {
            id
            title
            number
            createdAt
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
    org_created_at = None
    after = None
    while True:
        params = {"org": ORG_NAME, "first": PER_PAGE, "after": after}
        try:
            result = client.execute(query, variable_values=params)
        except Exception as e:
            logging.error(f"Error fetching Projects V2: {str(e)}")
            print(f"Error fetching Projects V2: {str(e)}")
            return None, None
        org = result.get("organization", {})
        if org_created_at is None:
            org_created_at = org.get("createdAt")
        projects_v2 = org.get("projectsV2", {})
        projects.extend(projects_v2.get("nodes", []))
        page_info = projects_v2.get("pageInfo", {})
        if not page_info.get("hasNextPage", False):
            break
        after = page_info.get("endCursor")
    logging.info(f"Fetched {len(projects)} projects")
    return projects, org_created_at
 
# Fetch repositories associated with a Project V2
def fetch_project_repositories(project_id):
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
                    createdAt
                  }
                }
                ... on PullRequest {
                  repository {
                    name
                    url
                    createdAt
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
            logging.error(f"Error fetching repositories for project {project_id}: {str(e)}")
            print(f"Error fetching repositories for project {project_id}: {str(e)}")
            return None
        items = result.get("node", {}).get("items", {}).get("nodes", [])
        for item in items:
            if item.get("content") and item["content"].get("repository"):
                repo = item["content"]["repository"]
                repositories.add((repo["name"], repo["url"], repo["createdAt"]))
        page_info = result.get("node", {}).get("items", {}).get("pageInfo", {})
        if not page_info.get("hasNextPage", False):
            break
        after = page_info.get("endCursor")
    logging.info(f"Fetched {len(repositories)} repositories for project {project_id}")
    return [{"name": name, "url": url, "created_at": created_at} for name, url, created_at in repositories]
 
# Main function
def main():
    fetch_time = datetime.now(timezone.utc)
    logging.info(f"Starting fetch at {fetch_time}")
 
    # Create or get Organization
    try:
        org = Organization.objects.get(name=ORG_NAME)
        created = False
        logging.info(f"Organization {ORG_NAME} already exists")
        print(f"Organization {ORG_NAME} already exists.")
    except DoesNotExist:
        api_success = False
        org_url = f"{REST_BASE_URL}/orgs/{ORG_NAME}"
        response = requests.get(org_url, headers=REST_HEADERS)
        check_rate_limit(response)
        org_created_at = fetch_time
        if response.status_code == 200:
            org_data = response.json()
            try:
                org_created_at = datetime.strptime(org_data.get('created_at'), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            except (ValueError, TypeError) as e:
                logging.error(f"Error parsing organization created_at: {str(e)}")
                print(f"Error parsing organization created_at: {str(e)}")
            api_success = True
        org = Organization.objects.create(
            name=ORG_NAME,
            total_repositories=0,
            total_projects=0,
            active_users_count=0,
            created_at=org_created_at,
            fetched_at=fetch_time if api_success else None
        )
        created = True
        logging.info(f"Created new Organization: {ORG_NAME}")
        print(f"Created new Organization: {ORG_NAME}")
    except MultipleObjectsReturned:
        logging.error(f"Multiple organizations found with name {ORG_NAME}")
        print(f"Error: Multiple organizations found with name {ORG_NAME}")
        raise
    except Exception as e:
        logging.error(f"Error accessing Organization: {str(e)}")
        print(f"Error accessing Organization: {str(e)}")
        raise
 
    # Fetch data
    repositories = fetch_repositories()
    members = fetch_members()
    projects, org_created_at = fetch_v2_projects()
 
    # Update organization created_at if not set
    if org_created_at and not created and not org.created_at:
        try:
            org_created_at_dt = datetime.strptime(org_created_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            org.created_at = org_created_at_dt
            update_fields = ['created_at']
            if not org.fetched_at:
                org.fetched_at = fetch_time
                update_fields.append('fetched_at')
            org.save(update_fields=update_fields)
            logging.info(f"Updated created_at for {org.name} to {org_created_at_dt}")
            print(f"Updated created_at for {org.name} to {org_created_at_dt}")
        except ValueError as e:
            logging.error(f"Error parsing organization created_at: {str(e)}")
            print(f"Error parsing organization created_at: {str(e)}")
 
    # Check if API calls were successful
    if repositories is None or members is None or projects is None:
        logging.error("One or more API calls failed. Skipping database updates.")
        print("One or more API calls failed. Skipping database updates.")
        return
 
    # Save all repositories (from REST API)
    repo_map = {}  # Map to track repositories and their fetched_at
    for repo_data in repositories:
        try:
            repo = Repository.objects.get(organization=org, name=repo_data['name'])
            repo_map[repo_data['name']] = repo
            update_fields = []
            api_success = True
            if repo.url != repo_data['html_url']:
                repo.url = repo_data['html_url']
                update_fields.append('url')
            try:
                new_created_at = datetime.strptime(repo_data['created_at'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                if repo.created_at != new_created_at:
                    repo.created_at = new_created_at
                    update_fields.append('created_at')
            except ValueError as e:
                logging.error(f"Error parsing created_at for repo {repo_data['name']}: {str(e)}")
                print(f"Error parsing created_at for repo {repo_data['name']}: {str(e)}")
                api_success = False
            if update_fields and api_success:
                # Only update fetched_at if it doesn't exist
                if not repo.fetched_at:
                    repo.fetched_at = fetch_time
                    update_fields.append('fetched_at')
                repo.save(update_fields=update_fields)
                logging.info(f"Updated repository {repo_data['name']} with fields {update_fields}")
            else:
                logging.info(f"No changes to repository {repo_data['name']}")
        except DoesNotExist:
            try:
                repo_created_at = datetime.strptime(repo_data['created_at'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            except ValueError as e:
                logging.error(f"Error parsing created_at for repo {repo_data['name']}: {str(e)}")
                print(f"Error parsing created_at for repo {repo_data['name']}: {str(e)}")
                repo_created_at = fetch_time
            repo = Repository.objects.create(
                organization=org,
                project=None,
                name=repo_data['name'],
                url=repo_data['html_url'],
                created_at=repo_created_at,
                fetched_at=fetch_time
            )
            repo_map[repo_data['name']] = repo
            logging.info(f"Created repository {repo_data['name']}")
        except NotUniqueError:
            logging.error(f"Repository {repo_data['name']} already exists for organization {ORG_NAME}")
            print(f"Repository {repo_data['name']} already exists for organization {ORG_NAME}")
            continue
        except MultipleObjectsReturned:
            logging.error(f"Multiple repositories found with name {repo_data['name']} for organization {ORG_NAME}")
            print(f"Error: Multiple repositories found with name {repo_data['name']} for organization {ORG_NAME}")
            raise
 
    # Save Users
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
            # Only update fetched_at if it doesn't exist
            if not user.fetched_at:
                user.fetched_at = fetch_time
                user.save(update_fields=['fetched_at'])
                logging.info(f"Updated fetched_at for user {username}")
            else:
                logging.info(f"User {username} already exists, no update needed")
        except DoesNotExist:
            email = fetch_user_email(username)
            api_success = email is not None
            user = User.objects.create(
                organization=org,
                username=username,
                email=email,
                created_at=fetch_time,
                fetched_at=fetch_time if api_success else None
            )
            logging.info(f"Created user {username}")
        except MultipleObjectsReturned:
            logging.error(f"Multiple users found with username {username}")
            print(f"Error: Multiple users found with username {username}")
            raise
 
    # Save Projects and associate repositories
    for project_data in projects:
        try:
            project = Project.objects.get(organization=org, number=project_data["number"])
            logging.info(f"Project {project_data['title']} (#{project_data['number']}) already exists, no update needed")
        except DoesNotExist:
            try:
                project_created_at = datetime.strptime(project_data["createdAt"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            except ValueError as e:
                logging.error(f"Error parsing created_at for project {project_data['title']}: {str(e)}")
                print(f"Error parsing created_at for project {project_data['title']}: {str(e)}")
                project_created_at = fetch_time
            project = Project.objects.create(
                organization=org,
                number=project_data["number"],
                name=project_data["title"],
                created_at=project_created_at,
                fetched_at=fetch_time
            )
            logging.info(f"Created project {project_data['title']} (#{project_data['number']})")
        except MultipleObjectsReturned:
            logging.error(f"Multiple projects found with number {project_data['number']} for organization {ORG_NAME}")
            print(f"Error: Multiple projects found with number {project_data['number']} for organization {ORG_NAME}")
            raise
 
        # Associate repositories with this project
        project_repos = fetch_project_repositories(project_data["id"])
        if project_repos is None:
            logging.warning(f"Skipping repositories for project {project_data['title']} due to API failure")
            print(f"Skipping repositories for project {project_data['title']} due to API failure.")
            continue
 
        for repo_data in project_repos:
            repo_name = repo_data["name"]
            if repo_name not in repo_map:
                logging.warning(f"Repository {repo_name} not found in organization repositories. Skipping.")
                print(f"Repository {repo_name} not found in organization repositories. Skipping.")
                continue
            repo = repo_map[repo_name]
            try:
                api_success = True
                if repo.project is None or repo.project.id != project.id:
                    repo.project = project
                    update_fields = ['project']
                    # Only update fetched_at if it doesn't exist
                    if not repo.fetched_at:
                        repo.fetched_at = fetch_time
                        update_fields.append('fetched_at')
                    repo.save(update_fields=update_fields)
                    logging.info(f"Associated repository {repo_name} with project {project.name}")
                else:
                    logging.info(f"Repository {repo_name} already associated with project {project.name}, no update needed")
            except MultipleObjectsReturned:
                logging.error(f"Multiple repositories found with name {repo_name} for organization {ORG_NAME}")
                print(f"Error: Multiple repositories found with name {repo_name} for organization {ORG_NAME}")
                raise
 
        # Save Teams and their members
        for team_data in project_data["teams"]["nodes"]:
            try:
                team = Team.objects.get(organization=org, project=project, name=team_data["name"])
                update_fields = []
                api_success = True
                team_users = []
                for member in team_data["members"]["nodes"]:
                    user = User.objects(organization=org, username=member["login"]).first()
                    if user:
                        team_users.append(user)
                if set(team_users) != set(team.users):
                    team.users = team_users
                    update_fields.append('users')
                    # Only update fetched_at if it doesn't exist
                    if not team.fetched_at:
                        team.fetched_at = fetch_time
                        update_fields.append('fetched_at')
                    team.save(update_fields=update_fields)
                    logging.info(f"Updated users for team {team_data['name']} in project {project.name}")
                else:
                    logging.info(f"No changes to users for team {team_data['name']} in project {project.name}")
            except DoesNotExist:
                team_users = []
                for member in team_data["members"]["nodes"]:
                    user = User.objects(organization=org, username=member["login"]).first()
                    if user:
                        team_users.append(user)
                team = Team.objects.create(
                    organization=org,
                    project=project,
                    name=team_data["name"],
                    users=team_users,
                    created_at=fetch_time,
                    fetched_at=fetch_time
                )
                logging.info(f"Created team {team_data['name']} for project {project.name}")
            except MultipleObjectsReturned:
                logging.error(f"Multiple teams found with name {team_data['name']} for project {project.name}")
                print(f"Error: Multiple teams found with name {team_data['name']} for project {project.name}")
                raise
 
    # Update Organization counts
    new_total_repos = Repository.objects(organization=org).count()
    new_total_projects = Project.objects(organization=org).count()
    new_active_users = User.objects(organization=org).count()
    update_fields = []
    if org.total_repositories != new_total_repos:
        org.total_repositories = new_total_repos
        update_fields.append('total_repositories')
    if org.total_projects != new_total_projects:
        org.total_projects = new_total_projects
        update_fields.append('total_projects')
    if org.active_users_count != new_active_users:
        org.active_users_count = new_active_users
        update_fields.append('active_users_count')
    if update_fields:
        # Only update fetched_at if it doesn't exist
        if not org.fetched_at:
            org.fetched_at = fetch_time
            update_fields.append('fetched_at')
        org.save(update_fields=update_fields)
        logging.info(f"Updated organization counts: Repos={org.total_repositories}, Projects={org.total_projects}, Users={org.active_users_count}")
    else:
        logging.info(f"No changes to organization counts for {org.name}")
 
    # Print summary
    print(f"Organization: {org.name}")
    print(f"Total Repositories: {org.total_repositories}")
    print(f"Total Projects: {org.total_projects}")
    print(f"Active Users: {org.active_users_count}")
    print("\nProjects:")
    for project in Project.objects(organization=org):
        print(f"\nProject: {project.name} (Number: {project.number})")
        print(f"Created At: {project.created_at}, Fetched At: {project.fetched_at}")
        repos = Repository.objects(project=project)
        print(f"Repositories: {len(repos)}")
        for repo in repos:
            print(f"  - {repo.name} ({repo.url}) [Created At: {repo.created_at}, Fetched At: {repo.fetched_at}]")
        teams = Team.objects(project=project)
        print(f"Teams: {len(teams)}")
        for team in teams:
            print(f"  - {team.name}: {', '.join(str(user) for user in team.users)}")
    print("\nActive Users:")
    for user in User.objects(organization=org):
        print(f"  Username: {user.username}, Email: {user.email or 'Not available'}, Created At: {user.created_at}")
    logging.info("Fetch completed successfully")
 
if __name__ == "__main__":
    main()