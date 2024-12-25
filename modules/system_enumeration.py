import subprocess
import os
import psutil
import getpass
import requests
import platform
import socket

# Network

def get_active_connections():
    try:
        result = subprocess.check_output("netstat -ano", shell=True, text=True)
        print(f"[INFO] Active Connections:\n{result}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Could not list active connections: {e}")
        return None


def get_network_config():
    try:
        result = subprocess.check_output("ipconfig /all", shell=True, text=True)
        print(f"[INFO] Network Config:\n{result}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Could not get network config: {e}")
        return None


def get_wifi_networks():
    try:
        result = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)
        print(f"[INFO] Wi-Fi Networks:\n{result}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Could not list Wi-Fi networks: {e}")
        return None


def get_mac_address():
    try:
        result = subprocess.check_output("getmac", shell=True, text=True)
        print(f"[INFO] MAC Addresses:\n{result}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Could not get MAC address: {e}")
        return None


# Files/drive related
def get_disk_usage():
    try:
        result = subprocess.check_output("wmic logicaldisk get size,freespace,caption", shell=True, text=True)
        print(f"[INFO] Disk Usage:\n{result}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Could not get disk usage: {e}")
        return None
    

def get_file_permissions(path):
    try:
        permissions = oct(os.stat(path).st_mode)[-3:]
        print(f"[INFO] File Permissions for {path}: {permissions}")
        return permissions
    except FileNotFoundError:
        print(f"[ERROR] File {path} not found.")
        return None
    
    
def list_files(directory="."):
    try:
        files = os.listdir(directory)
        print(f"[INFO] Files in {directory}: {files}")
        return files
    except FileNotFoundError:
        print(f"[ERROR] Directory {directory} not found.")
        return []

# processes related
def list_running_processes():
    processes = [(p.pid, p.name()) for p in psutil.process_iter(['pid', 'name'])]
    print(f"[INFO] Running Processes: {processes}")
    return processes


def get_process_details(pid):
    try:
        p = psutil.Process(pid)
        details = {
            "PID": pid,
            "Name": p.name(),
            "Status": p.status(),
            "Executable": p.exe(),
            "Memory": p.memory_info().rss
        }
        print(f"[INFO] Process Details: {details}")
        return details
    except psutil.NoSuchProcess:
        print(f"[ERROR] Process with PID {pid} not found.")
        return None

# users related
def get_current_user():
    user = getpass.getuser()
    print(f"[INFO] Current User: {user}")
    return user


def list_users():
    try:
        result = subprocess.check_output("net user", shell=True, text=True)
        users = result.splitlines()[4:-2]
        print(f"[INFO] Users: {users}")
        return users
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Could not list users: {e}")
        return []
    

# system related

def get_system_info():
    system_info = {
        "System": platform.system(),
        "Version": platform.version(),
        "Release": platform.release(),
        "Architecture": platform.architecture()[0],
        "Machine": platform.machine()
    }
    print(f"[INFO] System Info: {system_info}")
    return system_info


def get_os_version():
    os_version = platform.platform()
    print(f"[INFO] OS Version: {os_version}")
    return os_version


def get_public_ip():
    try:
        # Use IPv4-specific API
        ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
        print(f"[INFO] Public IP (IPv4): {ip}")
        return ip
    except requests.RequestException as e:
        print(f"[ERROR] Could not get public IP: {e}")
        return None

    
def get_hostname():
    hostname = socket.gethostname()
    print(f"[INFO] Hostname: {hostname}")
    return hostname


def run(functions):
    results = {}
    for func_name, params in functions.items():
        try:
            target_function = globals().get(func_name)
            if not callable(target_function):
                results[func_name] = "Function not found"
                print(f"[ERROR] Function '{func_name}' not found.")
                continue
            if isinstance(params, list):
                results[func_name] = target_function(*params)
            else:
                results[func_name] = target_function()
            print(f"[INFO] Executed {func_name}: {results[func_name]}")
        except Exception as e:
            print(f"[ERROR] Failed to execute {func_name}: {e}")
            results[func_name] = f"Error: {e}"
    return {"status": "success", "results": results}



# Run everything
if __name__ == "__main__":
    get_mac_address()
