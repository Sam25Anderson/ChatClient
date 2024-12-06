import socket
import threading

HOST = "127.0.0.1"  # Server's address

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
                print(message)
            else:
                break
        except ConnectionResetError:
            print("Connection to server lost.")
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    username = "Sam"
    client_socket.sendall(username.encode())  # Send username

    if dm == True:
        connected_client = input("Who do you want to message: ")
        client_socket.sendall(connected_client.encode())

    # Start a thread to listen for incoming messages
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input("Message: ")
        client_socket.sendall(message.encode())  # Send message to server
