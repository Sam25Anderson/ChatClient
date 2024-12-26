import socket
import threading
import time
from fastapi import FastAPI
import pickle

app = FastAPI()

HOST = "127.0.0.1" 
PORT = 12346

client_connections = {}
conn_dict = {}
current_connections = []
lock = threading.Lock()

def direct_message(sender, message):
    with lock:
        if sender in client_connections:
            conn = conn_dict.get(client_connections[sender])
            if conn and conn.fileno() != -1:
                try:
                    conn.sendall(message)
                except OSError as e:
                    print(f"Error sending message to {sender}: {e}")
            else:
                print(f"Invalid socket for {sender}. Cannot send message.")

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        try:
            conn.settimeout(10)
            data = conn.recv(1024)
            if not data:
                print(f"Connection closed by {addr}")
                return

            client_username = data.decode()
            print(f"Username: {client_username}")

            if len(current_connections) == 0:
                conn.sendall(pickle.dumps(["No other active users"]))
            else:
                conn.sendall(pickle.dumps(current_connections))
            
            current_connections.append(client_username)

            data = conn.recv(1024)
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
                try:
                    data = conn.recv(1024)
                    if not data:
                        print(f"Connection closed by {addr}")
                        break
                    direct_message(client_username, f"{client_username}: {data.decode()}".encode())
                except (ConnectionResetError, OSError) as e:
                    print(f"Error receiving data from {addr}: {e}")
                    break

        except ConnectionResetError:
            print(f"Error receiving data from {addr}: {e}")

        finally:
            with lock:
                if client_username in current_connections:
                    current_connections.remove(client_username)
                if client_username in client_connections:
                    del client_connections[client_username]
                if client_username in conn_dict:
                    del conn_dict[client_username]
                    
            direct_message(client_username, f"{client_username} left the chat.\n".encode())
            print(f"Closing connection to {addr}")

def start_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Socket server is running on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()

@app.on_event("startup")
def startup_event():
    threading.Thread(target=start_socket_server, daemon=True).start()

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running, and socket server is operational."}
