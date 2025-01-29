import socket
import threading
import pickle
import tkinter as tk
from tkinter import scrolledtext
import time

HOST = "127.0.0.1"
PORT = 12346


"""
1. Make the side buttons change the desired_user str value to that button name
2. Make a thread for each open chat
3. Store each chat data in seperate lists
4. Make clicking a button reprint the message history
    - Later maybe add some kind of caching to save time

"""


message_history = []
last_list_length = 0
sent_messages_history = 0
sent_messages = []
received_messages_history = 0
received_messages = []
current_chat = ""
button_count = 0
button_list = []
desired_user = ""
button_dict = {}

def receive_messages(client_socket):
    while True:
        try:
            if client_socket.fileno() == -1:
                print("Socket is closed.")
                break
            message = client_socket.recv(1024).decode()
            if message:
                message_history.append(message)
                received_messages.append(message)
                check_for_changes()
            else:
                print("Server closed the connection")
                break
        except ConnectionResetError:
            print("Connection lost to server")
            break
        except Exception as e:
            print(f"Error in receive_messages: {e}")
            break

def network_task():
    global last_list_length
    global message
    global sent_messages_history
    global sent_messages
    print("Network function started...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("Connected to server.")
        username = "John"
        client_socket.sendall(username.encode())

        other_user = pickle.loads(client_socket.recv(4096))
        for i in range(len(other_user)):
            print(other_user[i])
        
        connect_client = "Sam"
        client_socket.sendall(connect_client.encode())

        threading.Thread(target=receive_messages, args = (client_socket,), daemon=True).start()
        while True:
            if sent_messages_history < len(sent_messages):
                client_socket.sendall(message.encode())
                check_for_changes()

def update_chat_display():
    chat_display.configure(state=tk.NORMAL)
    chat_display.delete("1.0", tk.END)
    for i in message_history:
        chat_display.insert(tk.END, i + "\n")
    chat_display.see(tk.END)
    chat_display.configure(state=tk.DISABLED)

def check_for_changes():
    global last_list_length
    global received_messages_history
    global sent_messages_history
    if last_list_length < len(message_history) or received_messages_history < len(received_messages) or sent_messages_history < len(sent_messages):
        update_chat_display()
    last_list_length = len(message_history)
    received_messages_history = len(received_messages)
    sent_messages_history = len(sent_messages)

def start_network_thread():
    print("Starting network thread...")
    thread = threading.Thread(target = network_task, daemon=True)
    thread.start()

def set_message():
    global message
    message = user_input.get()
    if message.strip():
        user_input.set("")
        message_history.append(f"Me: {message}")
        sent_messages.append(message)
        return message
    return None

def receive_new_user_data(sock):
    try:
        data_length = int.from_bytes(sock.recv(4), "big")
        data = b""
        while len(data) < data_length:
            packet = sock.recv(data_length - len(data))
            if not packet:
                return None
            data += packet
        return pickle.loads(data)
    except Exception as e:
        print(f"Error receiving data: {e}")
        return None

def check_for_new_users():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as user_check_socket:
        user_check_socket.connect((HOST,PORT))
        socket_type = "user_check"
        user_check_socket.sendall(socket_type.encode())

        while True:
            user_list = receive_new_user_data(user_check_socket)
            for i in user_list:
                if i not in button_list:
                    add_button(i)
                    button_list.append(i)
            time.sleep(5)

def check_for_new_user_thread():
    print("Starting new user thread...")
    thread = threading.Thread(target = check_for_new_users, daemon=True)
    thread.start()

def change_chat(button_name):
    print(f"You clicked {button_dict[button_name]}")

#### GUI CODE ####

def add_button(button_name):
    global button_count
    global button_dict
    button_count += 1
    button_dict[button_name] = tk.Button(button_frame, text=f"{button_name}", command=lambda: change_chat(button_name)).pack(fill="x", pady=2)
    canvas.configure(scrollregion=canvas.bbox("all"))
    print(button_dict)

window = tk.Tk()
window.title("Chat Client")
window.minsize(400, 400)

window.columnconfigure(0, weight=0)  # Fix button list column width
window.columnconfigure(1, weight=2)  # Chat display
window.columnconfigure(2, weight=1)  # Send button
window.rowconfigure(0, weight=3)  # Main content
window.rowconfigure(1, weight=1)  # Message entry

button_frame = tk.Frame(window, width=100)
button_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(10, 0), pady=10)

button_frame.grid_propagate(False)
canvas = tk.Canvas(button_frame)
scrollbar = tk.Scrollbar(button_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")

inner_frame = tk.Frame(canvas)
inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Create the chat display
chat_display = scrolledtext.ScrolledText(window, state=tk.DISABLED)
chat_display.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=0, pady=10)

# Create the message entry
user_input = tk.StringVar()
message_entry = tk.Entry(window, textvariable=user_input)
message_entry.grid(row=1, column=1, sticky="ew", padx=0, pady=(0, 10))

# Create the send button
send_button = tk.Button(window, text="Send", command=set_message) 
send_button.grid(row=1, column=2, sticky="ew", padx=10, pady=(0, 10))


#### MAIN ####

check_for_new_user_thread()

#swap_chat_thread = threading.Thread(target = change_chat, daemon=True)
#swap_chat_thread.start()

start_network_thread()

window.mainloop()
    