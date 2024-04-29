import socket
from _thread import *
import sys

server = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Types of connections we can make

try: #This makes sure that you can connect "bind" into the server using the types of connections ^^
    s.bind((server,port))
except socket.error as e:
    str(e) #Passes the error 

s.listen(2)
print("Waiting for a connection, Server Started")

def threaded_client(conn):
    
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8") # Tells the console what language to understand the code in

            if not data: #If no data is being recieved
                print("Disconnected")
                break
            else:
                print("Recieved: ", reply)
                print("Sending: ", reply)
            conn.sendall(str.encode(reply)) #encodes data
        except:
            break


while True:
    conn, addr = s.accept() #accepts any connections 
    print("Connected to :", addr)

    start_new_thread((threaded_client, (conn,)))