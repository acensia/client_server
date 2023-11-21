import socket
import concurrent.futures
import time
from classes.classes import *


def handle_client(client_socket, client_address):
    client_socket.send(struct.pack('!i', MAP_SIZE))

    name = client_socket.recv(20).decode()
    if not name:
        print(f"Connection error on {client_address}")
        return

    P = player(name, client_socket)
    print(f"{name} entered.")
    game.online()
    info_data = client_socket.recv(5*8)
    if not info_data:
        print(f"Connection error on {client_address}")
        P.dest()
        return
    info = struct.unpack(f'{5}i', info_data)
    print(info)
    st = P.setLoc(info)
    # send pan state
    # if game starts, broadcast 


    P.setStat(info)
    game.now()
    # msg = f"Your state is) \nlocation : {P.x}, {P.y}\nstat : {P.atk}, {P.df}\npose : {P.pos}\n"
    # client_socket.send(msg.encode())
    # startSig = client_socket.recv(6).decode()
    # if not startSig:
    #     print("Sig error")

    while True:
        # Receive data from the client
        message = client_socket.recv(1024).decode()
        if not message:
            print(f"Connection error on {client_address}")
            P.dest()
            break

        if(message == "_quit"):
            client_socket.close()
            P.dest()
            break

        print(f"Received from client: {message}")
        i = int(message[0])
        j = int(message[3])
        P.getPan().putDol(P, i, j)
        # Send a response back to the client
        # client_socket.send(response.encode())


def main():
    # Define the host and the port on which to listen
    host = 'localhost'
    port = 3000
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        G = game()

         # to wait when server run right after terminated -> to run server on the same port 
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the address and port
        server_socket.bind((host, port))

        # Start listening for incoming connections
        server_socket.listen()

        print(f"Server listening on {host}:{port}")


        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            start = time.time()
            while True:
                # Accept a connection
                client_socket, client_address = server_socket.accept()       
                print(f"Connection from {client_address}")         
                executor.submit(handle_client, client_socket, client_address)

        # Close the server socket
        server_socket.close()

if __name__ == "__main__":
    main()
