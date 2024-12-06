import socket
import threading
import time
from fastapi import FastAPI

app = FastAPI()

HOST = "127.0.0.1" 
PORT = 12346

client_connections = {}
conn_dict = {}
lock = threading.Lock()

def direct_message(sender, message):
    with lock:
        if sender in client_connections:
            conn_dict[client_connections[sender]].sendall(message)

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        try:
            data = conn.recv(1024)  # Receive the username
            if not data:
                print(f"Connection closed by {addr}")
                return

            client_username = data.decode()
            print(f"Username: {client_username}")

            data = conn.recv(1024) # Receive the desired connection
            client_connection_request = data.decode()
            print(f"Connect request: {client_connection_request}")

            with lock:
                client_connections[client_username] = client_connection_request

            print(client_connections[client_username])
            print(client_connections)

            conn_dict[client_username] = conn

            while True:
                if client_connection_request not in client_connections:
                    print(f"Waiting for {client_connections[client_username]}")
                    time.sleep(3)
                else:
                    print(f"Connected with {client_connections[client_username]}")
                    break

            while True:
                data = conn.recv(1024)  # Receive data from the client
                if not data:
                    print(f"Connection closed by {addr}")
                    break
                direct_message(client_username, f"{client_username}: {data.decode()}\n".encode())

        except ConnectionResetError:
            print(f"Connection reset by {addr}")

        finally:
            direct_message(client_username, f"{client_username} left the chat.\n".encode())
            print(f"Closing connection to {addr}")

def start_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Socket server is running on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()  # Accept a client connection
            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()

@app.on_event("startup")
def startup_event():
    # Start the socket server in a background thread
    threading.Thread(target=start_socket_server, daemon=True).start()

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running, and socket server is operational."}