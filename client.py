from colorama import Fore, init
init()
import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 6000))

name = input("Enter your name: ")

def receive():
    while True:
        try:
            message = client.recv(1024).decode()

            if message == "NAME":
                client.send(name.encode())
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
        text = input("")
        if text.startswith("@"):
             message = text
        elif text.startswith("/"):
            message = text
        else:
            message = f"{name}: {text}"
        client.send(message.encode())

threading.Thread(target=receive).start()
threading.Thread(target=write).start()