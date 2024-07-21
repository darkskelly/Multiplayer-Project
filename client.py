import pygame
from network import Network
from player import Player
from loot import loot

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Penis")


def redrawWindow(win,players, loot_items):
    win.fill((255,255,255))
    for player in players.values():
        player.draw(win)
    for loot in loot_items:
        loot.draw(win)
    pygame.display.update()

def dict_to_player(data):
    """Convert a dictionary to a Player object."""
    if data is None:
        raise ValueError("Data for player conversion is None")
    return Player(
        x=data['x'],
        y=data['y'],
        width=data['width'],
        height=data['height'],
        colour=tuple(data['colour']),
        player_id=data['id']
    )
def dict_to_loot(data):
    """Convert a dictionary to a Loot object."""
    try:
        return loot(
            x=data['x'],
            y=data['y'],
            rarity=data['rarity'],
            colour=tuple(data['colour'])
        )
    except KeyError as e:
        print(f"Missing key in loot data: {e}")
        raise



def main():
    run = True
    n = Network()
    initial_data = n.getP()# player1_data should be a dictionary or a Player object

    if initial_data is None:
        print("Error: No initial data recieved.")
        return
    player1_data = initial_data.get('player')
    loot_data = initial_data.get('loot')
    
    if player1_data is None or loot_data is None:
        print("Error: Initial data is not in expected format.")
        return
    
    player1 = dict_to_player(player1_data)
    players = {player1.id: player1}
    

    try:
        loot_items = [dict_to_loot(item) for item in loot_data]
    except KeyError as e:
        print(f"Error converting loot data: {e}")
        return
    # if isinstance(player1_data, dict):
    #     try:
    #         player1 = dict_to_player(player1_data)
    #         print(f"Player1 initialised: {player1_data}")
    #     except ValueError as e:
    #         print(f"Error converting player1 data: {e}")
    #         return
    # else:
    #     print("Error: player1 data is not in expected format")
    #     return
    
    
    # Initialize player2 correctly based on player1's color
    # if hasattr(player1, 'colour'):
    #     player1.id = 0 if player1.colour == (255,0,0) else 1
    #     player2 = Player(0, 0, 50, 50, (0, 0, 255), player_id=1 if player1.id == 0 else 0)
    # else:
    #     print("Player1 doesn't have 'colour' attribute")


    clock = pygame.time.Clock()

    while run:
        clock.tick(120)
        data = n.send(player1)

        print(f"Recieved data from server: {data}")

        if data:
            players_data = data.get('players')
            loot_items_data = data.get('loot')
            
            try:
                loot_items = [dict_to_loot(item) for item in loot_items_data]
            except KeyError as e:
                print(f"Error converting loot data: {e}")
                continue
            for player_id, player_data in players_data.items():
                if player_id not in players:
                    players[player_id] = dict_to_player(player_data)
                else:
                    try:
                        # Update player2's attributes using dictionary keys
                        player = dict_to_player(player_data)
                        players[player.id].x = player.x
                        players[player.id].y = player.y
                        players[player.id].colour = player.colour
                        players[player.id].update()
                    except ValueError as e:
                            print(f"Error updating player ID: {player.id} data: {e}")
        else:
            print(f"Player data for id {player.id} is not  available")
        #    loot_items = [dict_to_loot(data) for data in loot_data]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        player1.move()
        redrawWindow(win, players, loot_items)
main()