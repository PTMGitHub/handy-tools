import requests

# Replace with your organization name and GitHub token
GITHUB_ORG = "hmrc"
TOKEN = ""  # You can use a GitHub token for authentication (optional)

# GitHub API endpoint for listing organization repositories
url = f"https://api.github.com/orgs/{GITHUB_ORG}/repos"

# Request headers with optional token
headers = {
    "Authorization": f"token {TOKEN}"  # Optional, only if you're using authentication
}

# Function to fetch and filter repositories
def get_repos_with_pbd():
    repos_with_pbd = []
    params = {
        "per_page": 100,  # To fetch up to 100 repos per page
        "page": 1         # Start from the first page
    }

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break
        
        repos = response.json()

        # Break if no more repos are returned
        if not repos:
            break

        # Filter repos with "pbd" or "PBD" in the name
        for repo in repos:
            if 'pbd' in repo['name'].lower():
                repos_with_pbd.append(repo['name'])

        # Go to the next page
        params['page'] += 1

    return repos_with_pbd

# Call the function and print the list of repos
repos_list = get_repos_with_pbd()
print(repos_list)