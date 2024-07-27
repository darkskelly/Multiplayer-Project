import socket
from _thread import start_new_thread
from player import Player
import pickle
from loot import loot
import random

server = "localhost"
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
        self.ready = {}
        self.connections = []
       # self.map_data = self.load_map_data()
        self.npcs = {}
        self.loot_items = []
        self.event_queue = []
        self.config = {
            "difficulty": "normal",
            "max_players": 10
        }
        self.player_spawn_points = [(0,0), (400,0), (255,255)]
        

    def generate_loot(self, num_items=5):
        for _ in range(num_items):
            x, y = random.randint(0, 490), random.randint(0, 490)

            rarity_value = random.randint(0, 100)
            if rarity_value <= 50:
                rarity = "common"
            elif rarity_value <= 75:
                rarity = "rare"
            elif rarity_value <= 90:
                rarity = "epic"
            else:
                rarity = "legendary"

            if rarity == "common":
                colour = (169, 169, 169)
                name = "common"
                item_value = 10
            elif rarity == "rare":
                colour =(0, 0, 255)
                name = "common"
                item_value = 10
            elif rarity == "epic":
                colour = (128, 0, 128)
                name = "common"
                item_value = 10
            elif rarity == "legendary":
                colour = (255, 215, 0)
                name = "common"
                item_value = 10
            
            loot_item = loot(x, y, rarity, colour, name, item_value)
            # Convert the loot object to a dictionary
            self.loot_items.append({
                'x': loot_item.x,
                'y': loot_item.y,
                'rarity': loot_item.rarity,
                'colour': loot_item.colour,
                'name': loot_item.name ,
                'item_value' : loot_item.item_value
            })

    #def load_map_data():
    #    pass
    
    def add_player(self, player_id, player):
        self.players[player_id] = player.__dict__ #returns player as a dictionary
        self.ready[player_id] = False
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
game_server.generate_loot()


def threaded_client(conn, player_id):
    global game_server
    conn.send(pickle.dumps({'player': game_server.players[player_id], 'loot': game_server.loot_items}))
    game_server.connections.append(conn)



    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            if not data: #If no data is being recieved
                print("Disconnected")
                break
            else:
                if data.get('type') == "ready":
                    game_server.ready[player_id] = True
                    both_ready = all(game_server.ready.values())
                    response = {"both ready": both_ready}
                    conn.sendall(pickle.dumps(response))
                    if both_ready:
                        game_server.game_state = "started"
                else:
                    # Update the player data on the server
                    game_server.players[player_id] = data
                    print("Recieved data from player {player_id}: {data}")
                    
                    # Send back all player data
                    reply = {'players': game_server.players, 'loot': game_server.loot_items}
                    conn.sendall(pickle.dumps(reply))
                    # for player_conn in game_server.players:
                    #     player_conn.sendall(pickle.dumps(reply)) #encodes data 
                    # print("Sending to player {player_id}: {data}")
        
        except Exception as e:
            print(f"Exception: {e}")
            break
    print("Lost connection")
    game_server.connections.remove(conn)
    conn.close()
    del game_server.players[player_id]
    del game_server.ready[player_id]
currentPlayer = 0
while True:
    conn, addr = s.accept() #accepts any connections 
    print("Connected to :", addr)

#assign player spawn points based on the player ID
    spawn_point = game_server.player_spawn_points[currentPlayer]
    if currentPlayer == 0:
        player = Player(spawn_point[0], spawn_point[1], 50, 50, (255, 0, 0), currentPlayer)
    else:
        player = Player(spawn_point[0], spawn_point[1], 50, 50, (0, 0, 255), currentPlayer)
    game_server.add_player(currentPlayer, player)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1