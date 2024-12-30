#client code
import socket
import threading

def receive_messages(s):
    """Handles receiving messages from the server."""
    while True:
        try:
            data = s.recv(1024)
            if data:
                # Print the received message
                print(f"\n{data.decode()}\n")
                
                # Prompt for input again
                print("Enter a message: ", end="", flush=True)
            else:
                break  # Server closed connection
        except Exception as e:
            print(f"\nError receiving data: {e}\n")
            break

def send_messages(s):
    """Handles sending messages to the server."""
    while True:
        try:
            message = input("Enter a message: ").strip()
            if message.lower() == "exit":
                print("\nExiting client...\n")
                break
            s.sendall(message.encode())
            print(f"\nYou sent: {message}\n")
        except KeyboardInterrupt:
            print("\n\nClient interrupted. Disconnecting...\n")
            break
        except Exception as e:
            print(f"\nError sending message: {e}\n")
            break

def start_client():
    HOST = "127.0.0.1"
    PORT = 65432

    # Prompt for the user's display name
    name = input("Enter your display name: ").strip()
    if not name:
        print("\nDisplay name cannot be empty.\n")
        return

    try:
        # Connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            # Send the display name to the server
            s.sendall(name.encode())

            # Start a thread to receive messages
            receive_thread = threading.Thread(target=receive_messages, args=(s,), daemon=True)
            receive_thread.start()

            # Start the main loop to send messages
            send_messages(s)

    except ConnectionRefusedError:
        print("\nUnable to connect to the server. Is it running?\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")

if __name__ == "__main__":
    start_client()
