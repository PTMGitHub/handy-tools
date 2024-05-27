import requests
import os

# Tou need to set ARTIFACTORY_ACCESS_TOKEN ARTIFACTORY_URL as
# per https://github.com/hmrc/build-and-deploy/blob/main/products/artifactory/terraform/README.md#working-in-lab03

# Next time print out the RAW group info

ARTIFACTORY_ACCESS_TOKEN = os.environ.get('ARTIFACTORY_ACCESS_TOKEN')
ARTIFACTORY_URL = os.environ.get('ARTIFACTORY_URL')
ENV = "live"
OUTPUT_FILE = "live_groups_module.tf"
OUTPUT_FILE2 = "live_groups_terraform_import.sh"

# Step 1: Make the first request to get group names
def get_group_names():
    url = f"{ARTIFACTORY_URL}/access/api/v2/groups/"
    headers = {"Authorization": f"Bearer {ARTIFACTORY_ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        groups = response.json()["groups"]
        return [group["group_name"] for group in groups]
    else:
        print("Error fetching group names:", response.text)
        return []


# Step 2: Make the second request for each group name
def get_group_info(group_name):
    url = f"{ARTIFACTORY_URL}/access/api/v2/groups/{group_name}"
    headers = {"Authorization": f"Bearer {ARTIFACTORY_ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching group info for {group_name}:", response.text)
        return None


# Main function
def main():
    group_names = get_group_names()
    if not group_names:
        return

    with open(OUTPUT_FILE, "w") as f:
        # Step 3: Output the result into a Terraform artifactory_group resource block
        for group_name in group_names:
            group_info = get_group_info(group_name)
            if group_info:
                f.write(f'module "{ENV}_{group_info.get("name", "").lower()}"{{\n')
                f.write(f'  source = "./modules/artifactory_group"\n')
                f.write(f'  build_environment = "{ENV}"\n')
                f.write(f'  name = "{group_info.get("name", "")}"\n')
                f.write(f'  description = "{group_info.get("description", "")}"\n')
                f.write(f'  auto_join = {group_info.get("auto_join", False)}\n')
                f.write(f'  admin_privileges = {group_info.get("admin_privileges", False)}\n')
                f.write('}\n\n')

    with open(OUTPUT_FILE2, "w") as f:
        # Step 4: Create a batch script to import the existing group terraform state
        for group_name in group_names:
            group_info = get_group_info(group_name)
            if group_info:
                f.write(f'aws-vault exec build-labs-RoleBuildEngineer -- terraform import module.{ENV}_{group_info.get("name", "").lower()}.artifactory_group.artifactory_group[0] {group_info.get("name", "").lower()}\n')


if __name__ == "__main__":
    main()
