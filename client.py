import socket
import threading

HOST = "127.0.0.1"  # Server's address
PORT = 12345        # Server's port

def receive_messages(client_socket):
    """Continuously receive and print messages from the server."""
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

    # Start a thread to listen for incoming messages
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input("Message: ")
        client_socket.sendall(message.encode())  # Send message to server
