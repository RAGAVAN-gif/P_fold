import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(("127.0.0.1", 6000))
server.listen()

print("Server running...")

clients = []
names = []
chat_history = []

def broadcast(message):
    for client in clients:
        client.send(message)
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode()


            if message == "/help":
                help_text = """
                Commands:
               /online  - show online users
                @name msg - private message
                /help - show commands
                """
                client.send(help_text.encode())

            # show online users
            if message == "/online":
                online_list = ", ".join(names)
                client.send(f"Online users: {online_list}".encode())

            # private message
            elif message.startswith("@"):
                parts = message.split(" ", 1)
                target_name = parts[0][1:]
                private_msg = parts[1]

                if target_name in names:
                    index = names.index(target_name)
                    target_client = clients[index]

                    sender_index = clients.index(client)
                    sender_name = names[sender_index]

                    target_client.send(
                        f"(Private) {sender_name}: {private_msg}".encode()
                    )

            # group chat
            else:
            
                chat_history.append(message)

                # keep only last 10 messages
                if len(chat_history) > 10:
                    chat_history.pop(0)

                broadcast(message.encode())

        except:
            index = clients.index(client)
            clients.remove(client)
            name = names[index]
            names.remove(name)

            broadcast(f"🔔 {name} left the chat".encode())
            client.close()
            break

while True:
    client, address = server.accept()
    print("Connected:", address)

    client.send("NAME".encode())
    name = client.recv(1024).decode()

    names.append(name)
    clients.append(client)
    client.send("---- Chat History ----".encode())

    for msg in chat_history:
        client.send(msg.encode())

    print(name, "joined the chat")

    broadcast(f"🔔 {name} joined the chat".encode())

    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()