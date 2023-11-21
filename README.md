# Client - Server Game

### 목차

#### [Outline](##1.-Outline)
#### [Server](##2.-Server)
#### [Client](##3.-Client)


## 1. Outline

#### Directory 구조

#### 통신 구조

Socket을 통한 TCP 통신

- 서버, 클라이언트의 양방향성을 위해 Socket 사용

- 안정적인 통신 확인을 위한 TCP 사용

## 2. Server

#### Socket

#### ThreadPool

#### Classes

##### 1. badukpan

##### 2. game

1. mat 

for map matrix

2. pan

 for matrix of badukpan

3. players

 for the number of players in game map

##### 3. player

1. init

2. setStat(self, info)

set stats of the player

3. setLoc(self, info)

locate the player in game.map

**send** the current state of the badukpan in the location

if the # of players in the location,

> broadcast starting signal by **sending**  0 and 1 for which color stone to use

> start the game in the location

4. move(self, i, j)

not used

5. dest(self)

print that the player quits

remove self from the location in game.mat and game.pans

6. getPan(self)

return the badukpan this player is in

7. sendInt, sendStr (self, v):

**send** variable v to the socket of the player



#### Functions

##### 1. handle_client(client_socket, client_address) 

1. **send** Map's size to the client, checking the server properly connected

2. *receive* the player's name

3. *receive* the player's information

4. with the info, make a Player class

5. wait for the client's message

## 3. Client 

#### Socket

#### Functions



## 4. Issues

#### Socket

1. transporting string

python : encode & decode string

c++ : with const char *, size

2. transporting int (& int array)

python : struct.pack('!i', var) & unpack

c++ : with const int *, ntohl(var) on receiving

3. detecting socket unconnection

check return value of send & recv

