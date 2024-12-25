import socket
import threading
import pickle
import tkinter as tk
from tkinter import scrolledtext

HOST = "127.0.0.1"
PORT = 12346

message_history = []
last_list_length = 0

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                message_history.append(message)
                update_chat_display()
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
    print("Network function started...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("Connected to server.")
        username = "Sam"
        client_socket.sendall(username.encode())

        other_user = pickle.loads(client_socket.recv(4096))
        for i in range(len(other_user)):
            print(other_user[i])
        
        connect_client = "Brad"
        client_socket.sendall(connect_client.encode())

        threading.Thread(target=receive_messages, args = (client_socket,), daemon=True).start()
        while True:
            if last_list_length < len(message_history):
                client_socket.sendall(message.encode())
                update_chat_display()
                last_list_length = len(message_history)

def update_chat_display():
    chat_display.configure(state=tk.NORMAL)
    chat_display.delete("1.0", tk.END)
    for i in message_history:
        chat_display.insert(tk.END, i + "\n")
    chat_display.see(tk.END)
    chat_display.configure(state=tk.DISABLED)

def check_for_changes():
    global last_list_length
    if last_list_length < len(message_history):
        window.after(100, update_chat_display)
    last_list_length = len(message_history)

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
        return message
    return None

#### GUI CODE ####

def add_button(button_name):
    global button_count
    button_count += 1
    tk.Button(button_frame, text=f"{button_name}").pack(fill="x", pady=2)
    canvas.configure(scrollregion=canvas.bbox("all"))

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

button_count = 0
add_button("Test")  # Example buttons
add_button("Big testerson")

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

start_network_thread()

window.after(100, check_for_changes)
window.mainloop()
    