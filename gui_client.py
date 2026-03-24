import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 6000))

name = input("Enter your name: ")

# GUI
window = tk.Tk()
window.title("Chat App")

chat_area = scrolledtext.ScrolledText(window)
chat_area.pack(padx=10, pady=10)

msg_entry = tk.Entry(window, width=50)
msg_entry.pack(padx=10, pady=5)

def send_file():
    filepath = filedialog.askopenfilename()

    if not filepath:
        return

    try:
        with open(filepath, "rb") as f:
            data = f.read()

        filename = os.path.basename(filepath)

        client.send(f"FILE|{filename}|".encode() + data)

        chat_area.insert(tk.END, f"You sent file: {filename}\n")
        chat_area.yview(tk.END)

    except:
        chat_area.insert(tk.END, "Error sending file\n")

def send_message():
    text = msg_entry.get()

    if text == "":
        return

    if text.startswith("@") or text.startswith("/"):
        message = text
    else:
        message = f"{name}: {text}"

    client.send(message.encode())
    msg_entry.delete(0, tk.END)

send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack(pady=5)
file_button = tk.Button(window, text="📁 Send File", command=send_file)
file_button.pack(pady=5)

def receive():
    while True:
        try:
            message = client.recv(1024).decode(errors="ignore")

            if message == "NAME":
                client.send(name.encode())

            elif message.startswith("FILE|"):
                parts = message.split("|", 3)

                sender = parts[1]
                filename = parts[2]
                filedata = parts[3].encode()

                with open(f"received_{filename}", "wb") as f:
                    f.write(filedata)

                def update_chat():
                    chat_area.insert(tk.END, f"{sender} sent file: {filename}\n")
                    chat_area.yview(tk.END)

                window.after(0, update_chat)

            else:
                def update_chat():
                    chat_area.insert(tk.END, message + "\n")
                    chat_area.yview(tk.END)

                window.after(0, update_chat)

        except:
            break
window.mainloop()
threading.Thread(target=receive).start()
