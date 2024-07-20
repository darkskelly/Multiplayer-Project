import socket
from _thread import start_new_thread
from player import Player
import pickle
from loot import loot

server = "192.168.1.119"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Types of connections we can make

try: #This makes sure that you can connect "bind" into the server using the types of connections ^^
    s.bind((server,port))
except socket.error as e:
    str(e) #Passes the error 

s.listen(2)
print("Waiting for a connection, Server Started")


class GameServer:
    def __init__(self):
        self.players = {} # This is where data about the players is stored
        self.game_state = "waiting"
       # self.map_data = self.load_map_data()
        self.npcs = {}
        self.items = {}
        self.event_queue = []
        self.config = {
            "difficulty": "normal",
            "max_players": 10
        }

    #def load_map_data():
    #    pass
    
    def add_player(self, player_id, player):
        self.players[player_id] = player.__dict__ #returns player as a dictionary
        event = {
            "type": "EVENT_TYPE_ADD_PLAYER",
            "player_id": player_id,
            "player": player.__dict__
        }
        self.event_queue.append(event)
       # print(f"Added player: {player.name}")
    
    def process_events(self):
        while self.event_queue:
            event = self.event_queue.pop(0)
            self.handle_event(event)

    def handle_event(self, event):
        if event["type"] == "EVENT_TYPE_ADD_PLAYER":
            player_id = event["player_id"]
            player = event["player"]
            self.players[player_id] = player
       #     print(f"Added player: {player.name}")



game_server = GameServer()



def threaded_client(conn, player_id):
    global game_server
    conn.send(pickle.dumps(game_server.players[player_id]))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))


            if not data: #If no data is being recieved
                print("Disconnected")
                break
            else:

                # Update the player data on the server
                game_server.players[player_id] = data
                print("Recieved data from player {player_id}: {data}")
                
                # Send back all player data
                reply = game_server.players
                conn.sendall(pickle.dumps(reply)) #encodes data
                print("Sending to player {player_id}: {data}")
        
        except Exception as e:
            print(f"Exception: {e}")
            break
    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept() #accepts any connections 
    print("Connected to :", addr)
    if currentPlayer == 0:
        player = Player(0, 0, 50, 50, (255, 0, 0), currentPlayer)
    else:
        player = Player(0,0, 50, 50, (0, 0, 255), currentPlayer)
    game_server.add_player(currentPlayer, player)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1