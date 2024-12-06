import socket
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

# Configuration for the socket server
HOST = "127.0.0.1"  # Localhost
PORT = 12345        # Port to listen on

def start_socket_server():
    """Starts the socket server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Socket server is running on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()  # Accept a client connection
            print(f"Connected by {addr}")
            with conn:
                data = conn.recv(1024)
                print(f"Username: {data.decode()}")
                client_username = data.decode()
                while True:
                    data = conn.recv(1024)  # Receive data
                    if not data:
                        break
                    print(f"{client_username}: {data.decode()}")
                    conn.sendall(b"Message received!")  # Send a response

@app.on_event("startup")
def startup_event():
    """Runs when FastAPI starts."""
    # Start the socket server in a background task
    import threading
    threading.Thread(target=start_socket_server, daemon=True).start()

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running, and socket server is operational."}
