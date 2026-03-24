from colorama import Fore, init
init()
import socket
import threading
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 6000))

name = input("Enter your name: ")

def receive():
    while True:
        try:
            message = client.recv(1024).decode(errors="ignore")

            #  1. FILE HANDLING (FIRST)
            if message.startswith("FILE|"):
                parts = message.split("|", 3)

                sender = parts[1]
                filename = parts[2]
                filedata = parts[3].encode()

                with open(f"received_{filename}", "wb") as f:
                    f.write(filedata)

                print(Fore.YELLOW + f"{sender} sent file: {filename}")

            # 2. NAME HANDSHAKE
            elif message == "NAME":
                client.send(name.encode())

            # 3. NORMAL MESSAGES
            else:
                if "(Private)" in message:
                    print(Fore.MAGENTA + message)
                elif "joined the chat" in message:
                    print(Fore.GREEN + message)
                elif "left the chat" in message:
                    print(Fore.RED + message)
                else:
                    print(Fore.WHITE + message)

        except:
            break

def write():
    while True:
        text = input("").strip()

        if text == "":
            continue

        # send file
        if text.startswith("/file"):
            filepath = text.split(" ", 1)[1]

            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    data = f.read()

                filename = os.path.basename(filepath)

                client.send(f"FILE|{filename}|".encode() + data)
            else:
                print("File not found")

        else:
            client.send("TYPING".encode())

            if text.startswith("@"):
                message = text
            elif text.startswith("/"):
                message = text
            else:
                message = f"{name}: {text}"

            client.send(message.encode())
threading.Thread(target=receive).start()
threading.Thread(target=write).start()