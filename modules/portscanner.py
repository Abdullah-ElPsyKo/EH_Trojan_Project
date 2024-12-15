import socket
import threading 
from queue import Queue 
import time
import subprocess

print_lock = threading.Lock()
q = Queue()

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        with print_lock:
            if result == 0:
                print(f"Port {port} is OPEN.")
                return True
            else:
                print(f"Port {port} is CLOSED.")
                return False
    except Exception as e:
        print(f"Could not scan the port: {port} Error: {e}")
        return False
    finally:
        s.close()
        

def scan_target(ip, ports=[], range_from=0, range_to=0, threaded=False):
    open_ports = []
    if range_from == 0 and range_to == 0:
        if threaded:
            multi_threaded_scan(ip, ports)
        else:
            for port in ports:
                if scan_port(ip, port):
                    open_ports.append(port)
    else:
        ports_to_scan = list(range(range_from, range_to + 1))
        if threaded:
            multi_threaded_scan(ip, ports_to_scan)
        else:
            for port in ports_to_scan:
                if scan_port(ip, port):
                    open_ports.append(port)

    return open_ports


def scan_common_ports(ip, threaded=False):
    common_ports = [21, 22, 25, 53, 67, 68, 80, 110, 123, 143, 443, 465, 631, 993, 995, 3306, 3389, 8080]
    if threaded:
        multi_threaded_scan(ip, common_ports)
    else:
        open_ports = []
        for port in common_ports:
            if scan_port(ip, port):
                open_ports.append(port)
        print(f"[INFO] Open common ports: {open_ports}")


def threader(ip):
    while True:
        port = q.get()
        scan_port(ip, port)
        q.task_done()


def multi_threaded_scan(ip, ports, num_threads=4):
    for x in range(num_threads):
        t = threading.Thread(target=threader, args=(ip,))
        t.daemon = True
        t.start()

    start = time.time()

    for port in ports:
        q.put(port)

    q.join()
    print(f"[INFO] Scan completed in {round(time.time() - start, 2)} seconds")


def discover_ips(subnet, timeout=1):
    active_ips = []
    print(f"Discovering devices on {subnet}.0/24...")

    def ping_ip(ip):
        try:
            result = subprocess.run(
                ["ping", "-n", "1", "-w", str(timeout * 1000), ip],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if result.returncode == 0:
                with print_lock:
                    print(f"[ACTIVE] Found live IP: {ip}")
                active_ips.append(ip)
        except Exception as e:
            print(f"[ERROR] Failed to ping {ip}: {e}")

    threads = []
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        t = threading.Thread(target=ping_ip, args=(ip,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"[INFO] Active IPs found: {active_ips}")
    return active_ips



def detect_os(ips, timeout=1):
    ip_OS = []
    for ip in ips:
        result = subprocess.run(
                    ["ping", "-n", "1", "-w", str(timeout * 1000), ip],
                    stdout=subprocess.PIPE,  # Redirect output
                    stderr=subprocess.PIPE,  # Redirect error
                )
        output = result.stdout.decode("utf-8")
        for line in output.splitlines():
            if "TTL=" in line:
                ttl_val = int(line.split("TTL=")[1].strip())
                if ttl_val == 128:
                    ip_OS.append(f"{ip}: Windows")
                elif ttl_val == 64:
                    ip_OS.append(f"{ip}: Linux/Unix/macOS")
                elif ttl_val == 255:
                    ip_OS.append(f"{ip}: Network Device")
                else:
                    ip_OS.append(f"{ip}: Unknown TTL={ttl_val}")
    for os in ip_OS:
        print(f"[INFO] {os}")
    return ip_OS


def get_ip_details(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        print(f"[INFO] IP Details for {ip}: Hostname - {hostname}")
        return {"IP": ip, "Hostname": hostname}
    except socket.herror:
        print(f"[ERROR] no details found for IP: {ip}")
        return {"IP": ip, "Hostname": "Unknown"}



if __name__ == "__main__":
    # detect_os(discover_ips("192.168.1"))
    get_ip_details("192.168.1.2")