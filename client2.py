import socket

# Configuration for connecting to the server
HOST = "127.0.0.1"  # Server's address
PORT = 12345        # Server's port

client_username = "Brad"
print('Type "End" to leave the chat')

def client_message():
    clientMessage = input("Message to send to server: ")
    return clientMessage

def client_send_receive():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))  # Connect to the server
        print(f"Connected to server at {HOST}:{PORT}")
            
        client_socket.sendall(client_username.encode()) # Sending the username
        
        while True:
            message = client_message()

            if message == "End":
                break

            client_socket.sendall(message.encode())  # Send a message                
            data = client_socket.recv(1024)  # Receive a response
            print(f"Received: {data.decode()}")
        

if __name__ == "__main__":
    client_send_receive()
