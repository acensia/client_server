import socket
import concurrent.futures
import struct
import time

MAP_SIZE = 10

class game:
    mat = [[[] for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    players = 0
    def __init__(self) -> None:
        pass

    def now():
        for i in game.mat:
            for j in i:
                print(f"{len(j):>{2}}", end=" ")
            print()
    
    def online():
        print(f"{game.players} is online")
        return game.players



class player(game):
    def __init__(self, name) -> None:
        self.name = name
        game.players += 1
        self.x = -1

    def setStat(self, info):
        self.atk = info[2]
        self.df = info[3]
        self.pos = info[4]

    def setLoc(self, info):
        self.x = info[0]
        self.y = info[1]
        game.mat[self.x][self.y].append(self.name)
    

    def move(self, i, j):
        self.x = (self.x + i + MAP_SIZE) % MAP_SIZE
        self.y = (self.y + j + MAP_SIZE) % MAP_SIZE

    def dest(self):
        print(f"Player \"{self.name}\" has quit")
        if self.x != -1:
            game.mat[self.x][self.y].remove(self.name)
        game.players -= 1


def handle_client(client_socket, client_address):
    client_socket.send(struct.pack('!i', MAP_SIZE))

    name = client_socket.recv(20).decode()
    if not name:
        print(f"Connection error on {client_address}")
        return

    P = player(name)
    print(f"{name} entered.")
    game.online()
    info_data = client_socket.recv(5*8)
    if not info_data:
        print(f"Connection error on {client_address}")
        P.dest()
        return
    info = struct.unpack(f'{5}i', info_data)
    P.setLoc(info)
    P.setStat(info)
    game.now()
    msg = f"Your state is) \nlocation : {P.x}, {P.y}\nstat : {P.atk}, {P.df}\npose : {P.pos}\n"
    client_socket.send(msg.encode())
    # print(msg)

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

        # Send a response back to the client
        response = "Hello from the server!"
        client_socket.send(response.encode())


def main():
    # Define the host and the port on which to listen
    host = 'localhost'
    port = 3000
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        G = game()
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
