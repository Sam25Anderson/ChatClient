import socket
import threading
import os
import pickle

HOST = "127.0.0.1" 

chat_history = []

desired_chat = input("General of direct message (G/D): ")
if desired_chat == "G":
    dm = False
    PORT = 12345
else:
    dm = True
    PORT = 12346

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                os.system('cls')
                for i in range(len(chat_history)):
                    print(chat_history[i])
                chat_history.append(message)
                print(message)
            else:
                break
        except ConnectionResetError:
            print("Connection to server lost.")
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    username = "Sam"
    client_socket.sendall(username.encode()) 

    if dm == True:
        other_users = pickle.loads(client_socket.recv(4096))
        for i in range(len(other_users)):
            print(other_users[i])

    if dm == True:
        connected_client = input("Who do you want to message: ")
        client_socket.sendall(connected_client.encode())

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input()
        chat_history.append(f"Me: {message}")
        client_socket.sendall(message.encode()) 
