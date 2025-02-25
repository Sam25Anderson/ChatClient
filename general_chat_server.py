import socket
import threading
from fastapi import FastAPI

app = FastAPI()

# Configuration for the socket server
HOST = "127.0.0.1"  # Localhost
PORT = 12345        # Port to listen on

clients = []
lock = threading.Lock()  # To make `clients` thread-safe

def broadcast(sender_conn, message):
    with lock:  # Ensure thread-safe access to clients
        for client_conn, _, _ in clients:
            if client_conn != sender_conn:
                try:
                    client_conn.sendall(message)
                except Exception:
                    clients.remove((client_conn, _, _))

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        try:
            data = conn.recv(1024)
            if not data:
                print(f"Connection closed by {addr}")
                return

            client_username = data.decode()
            print(f"Username: {client_username}")

            with lock:
                clients.append((conn, addr, client_username))

            # Notify other clients
            broadcast(conn, f"{client_username} joined the chat.\n".encode())

            while True:
                data = conn.recv(1024) 
                if not data:
                    print(f"Connection closed by {addr}")
                    break
                broadcast(conn, f"{client_username}: {data.decode()}\n".encode())

        except ConnectionResetError:
            print(f"Connection reset by {addr}")

        finally:
            with lock:
                clients.remove((conn, addr, client_username))
            broadcast(conn, f"{client_username} left the chat.\n".encode())
            print(f"Closing connection to {addr}")

def start_socket_server():
    """Starts the socket server."""
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
