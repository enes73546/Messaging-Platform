#add this code as your server
import socket
import threading

clients = {}  # Dictionary to store clients and their names

def handle_client(conn, addr):
    """Handles communication with a single client."""
    try:
        # Receive and store the client's name
        name = conn.recv(1024).decode()
        clients[conn] = name
        broadcast(f"\n\n{name} has joined the chat!\n", conn)

        while True:
            # Receive messages from the client
            data = conn.recv(1024)
            if data:
                # Broadcast the message to other clients
                message = f"{name}: {data.decode()}"
                broadcast(message, conn)
            else:
                break
    except Exception as e:
        print(f"\nError with client {addr}: {e}\n")
    finally:
        # Remove the client and notify others
        if conn in clients:
            broadcast(f"\n\n{clients[conn]} has left the chat.\n", conn)
            del clients[conn]
        conn.close()

def broadcast(message, sender_conn=None):
    """Sends a message to all clients except the sender."""
    for conn in clients:
        if conn != sender_conn:
            try:
                conn.sendall(message.encode())
            except Exception as e:
                print(f"\nError sending to client: {e}\n")

def start_server():
    HOST = "127.0.0.1"
    PORT = 65432

    print("Starting server...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print("Server is running. Waiting for connections...")
        while True:
            conn, addr = server.accept()
            print(f"Connected by {addr}")
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
