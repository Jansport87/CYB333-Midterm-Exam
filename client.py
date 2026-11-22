import socket

# Server connection settings
HOST = "127.0.0.1"  # Server IP address
PORT = 65432        # Server port

def start_client():
    try:
        # Initialize the client socket using IPv4 and TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

            # Set a timeout to prevent indefinite waiting
            client_socket.settimeout(10)

            # Connect to the server
            client_socket.connect((HOST, PORT))

            print("Successfully connected to the server.")

            # Send a message to the server
            message = "Hello Server! This is the Python client."
            client_socket.sendall(message.encode("utf-8"))

            # Receive the server's response
            response = client_socket.recv(1024)

            print("Server response:", response.decode("utf-8"))

    # Handle connection errors
    except ConnectionRefusedError:
        print("Connection failed: Server is not running.")

    # Handle timeout errors
    except socket.timeout:
        print("Connection timed out.")

    # Handle socket errors
    except OSError as error:
        print(f"Socket error: {error}")

    # Handle any unexpected exceptions
    except Exception as error:
        print(f"Unexpected client error: {error}")

if __name__ == "__main__":
    start_client()