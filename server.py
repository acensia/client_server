import socket

def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Define the host and the port on which to listen
    host = 'localhost'
    port = 3000

    # Bind the socket to the address and port
    server_socket.bind((host, port))

    # Start listening for incoming connections
    server_socket.listen()

    print(f"Server listening on {host}:{port}")
    # Accept a connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    while True:
        # Receive data from the client
        message = client_socket.recv(1024).decode()
        if(message == "_quit"):
            client_socket.send("_quit".encode())
            break

        print(f"Received from client: {message}")

        # Send a response back to the client
        response = "Hello from the server!"
        client_socket.send(response.encode())

    # Close the client connection
    client_socket.close()

    # Close the server socket
    server_socket.close()

if __name__ == "__main__":
    main()
