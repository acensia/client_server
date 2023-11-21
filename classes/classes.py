import struct

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
        print(i, j)
        print(i*9 + j)
        if not self.ing:
            print("Wrong signal?")
            return
        if p.name == self.p1.name:
            self.pan[i][j] = '*'
            self.p2.sock.send(struct.pack('!i', i*9 + j))
        else :
            self.pan[i][j] = 'o'
            self.p1.sock.send(struct.pack('!i', i*9 + j))
        self.showPan()

    def start(self, p1, p2):
        self.ing = True
        self.p1 = p1
        self.p2 = p2
        p1.sock.send(struct.pack('!i', -1))

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
        if len(game.mat[self.x][self.y]) == 2:
            print("Game in {}, {} starts".format(self.x, self.y))
            for i, p in enumerate(game.mat[self.x][self.y]):
                p.sendInt(i)
            game.baduk_start(self.x, self.y)
            return True
        return False

    def move(self, i, j):
        self.x = (self.x + i + MAP_SIZE) % MAP_SIZE
        self.y = (self.y + j + MAP_SIZE) % MAP_SIZE

    def dest(self):
        print(f"Player \"{self.name}\" has quit")
        if self.x != -1:
            game.mat[self.x][self.y].remove(self)
            game.pans[self.x][self.y].out(self)
        game.players -= 1

    def getPan(self):
        return game.pans[self.x][self.y]
    
    def sendInt(self, i):
        self.sock.send(struct.pack('!i', i))
    def sendStr(self, st):
        self.sock.send(st.encode())