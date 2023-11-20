import socket
import concurrent.futures
import struct
import time

MAP_SIZE = 2

class badukpan :
    def __init__(self, size):
        self.pan = [['+' for _ in range(size)] for _ in range(size)]
        self.p1 = None
        self.p2 = None
        self.ing = False

    def showPan(self):
        res = ""
        for r in self.pan:
            for c in r:
                print(c, end=' ')
                res += c
            print('')
        return res
    
    def putDol(self, p, i, j):
        if not self.ing:
            return
        if p.name == self.p1.name:
            self.pan[i][j] = '*'
            self.p2.sock(struct.pack('!i', 1))
        else :
            self.pan[i][j] = 'o'
            self.p1.sock(struct.pack('!i', 0))
        self.showPan()

    def start(self, p1, p2):
        self.ing = True
        self.p1 = p1
        self.p2 = p2

    def out(self, p):
        if self.p1 == p:
            p1 = ""
        else :
            p2 = ""
        self.ing = False

class game:
    mat = [[[] for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    pans = [[badukpan(9) for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
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
    
    def baduk_start(i, j):
        game.pans[i][j].start(game.mat[i][j][0], game.mat[i][j][1])

class player:
    def __init__(self, name, sock=None) -> None:
        self.name = name
        game.players += 1
        self.x = -1
        self.sock = sock

    def setStat(self, info):
        self.atk = info[2]
        self.df = info[3]
        self.pos = info[4]

    def setLoc(self, info):
        self.x = info[0]
        self.y = info[1]
        game.mat[self.x][self.y].append(self)
        msg = self.getPan().showPan()
        print(msg)
        self.sendStr(msg)
        print(len(game.mat[self.x][self.y]))
        if len(game.mat[self.x][self.y]) == 2:
            game.baduk_start(self.x, self.y)
            print("Game in {}, {} starts".format(self.x, self.y))
            for i, p in enumerate(game.mat[self.x][self.y]):
                p.sendInt(i)
                print(i)
            return True
        return False
    

    def move(self, i, j):
        self.x = (self.x + i + MAP_SIZE) % MAP_SIZE
        self.y = (self.y + j + MAP_SIZE) % MAP_SIZE

    def dest(self):
        print(f"Player \"{self.name}\" has quit")
        if self.x != -1:
            game.mat[self.x][self.y].remove(self.name)
            game.pans[self.x][self.y].out(self.name)
        game.players -= 1

    def getPan(self):
        return game.pans[self.x][self.y]
    
    def sendInt(self, i):
        self.sock.send(struct.pack('!i', i))
    def sendStr(self, st):
        self.sock.send(st.encode())

    def sameP(p1, p2):
        return p1.name == p2.name

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
    startSig = client_socket.recv(6).decode()
    if not startSig:
        print("Sig error")
    

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
        P.getPan().putDol(i, j)
        # Send a response back to the client
        response = P.getPan().showPan()
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
