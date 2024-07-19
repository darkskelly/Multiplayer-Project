import socket
from _thread import *
from player import Player
import pickle
server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Types of connections we can make

try: #This makes sure that you can connect "bind" into the server using the types of connections ^^
    s.bind((server,port))
except socket.error as e:
    str(e) #Passes the error 

s.listen(2)
print("Waiting for a connection, Server Started")


players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(0,0,255))] #Player Objects on the server

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data: #If no data is being recieved
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Recieved: ", data)
                print("Sending: ", reply)
            conn.sendall(pickle.dumps(reply)) #encodes data
        except:
            break
    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept() #accepts any connections 
    print("Connected to :", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1