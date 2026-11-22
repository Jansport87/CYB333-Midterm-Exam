import socket

# Server configuration
HOST = "127.0.0.1"  # Localhost IP address
PORT = 65432        # Port to listen on

def start_server():
    # Initialize the server socket using IPv4 and TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # Allow the address to be reused after restarting the server
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            # Bind the socket to the specified IP and port
            server_socket.bind((HOST, PORT))

            # Listen for incoming connections
            server_socket.listen()

            print(f"Server listening on {HOST}:{PORT}")

            # Accept an incoming client connection
            conn, addr = server_socket.accept()

            with conn:
                print(f"Connected by {addr}")

                # Receive data from the client
                data = conn.recv(1024)

                if data:
                    message = data.decode("utf-8")
                    print(f"Client says: {message}")

                    # Send a response back to the client
                    response = "Message received successfully!"
                    conn.sendall(response.encode("utf-8"))

        # Handle socket errors
        except OSError as error:
            print(f"Server socket error: {error}")

        # Handle any unexpected exceptions
        except Exception as error:
            print(f"Unexpected server error: {error}")

        #Disconnect the client and close the server socket
        finally:
            print("Server shutting down.")

if __name__ == "__main__":
    start_server()
