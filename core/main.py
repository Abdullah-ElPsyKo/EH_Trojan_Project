import json
from github import Github

# Load github token
GITHUB_TOKEN = "token"
REPO_NAME = "yourusername/yourrepository"
CONFIG_FILE = "config/config.json"
DATA_DIR = "data"

# Initialize client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

def download_config():
    contents = repo.get_contents(CONFIG_FILE)
    config_data = json.loads(contents.decoded_content.decode())
    print(f"[INFO] Downloaded Config: {config_data}")
    return config_data

if __name__ == "__main__":
    config = download_config()