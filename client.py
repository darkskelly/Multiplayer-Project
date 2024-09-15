import pygame
from network import Network
from player import Player
from loot import loot

width = 500
height = 500
STAT_POINTS = 10
START_BG_COLOUR = (0, 100, 0)  # Dark Green
STAT_BUTTON_WIDTH = 150
STAT_BUTTON_HEIGHT = 40
BUTTON_MARGIN = 10
FONT_SIZE = 20
READY_BUTTON_WIDTH = 200
READY_BUTTON_HEIGHT = 50
READY_BUTTON_COLOUR = (0, 200, 0)  # Green
READY_BUTTON_COLOUR_NOT_READY = (200, 0, 0)  # Red
TEXT_COLOUR = (255, 255, 255)  # White

pygame.font.init()
FONT = pygame.font.SysFont('comicsans', FONT_SIZE)

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Penis")

def draw_text(win,text, position, colour=TEXT_COLOUR):
    label = FONT.render(text, True, colour)
    win.blit(label, position)

def draw_button(win, rect, text, colour=READY_BUTTON_COLOUR):
    pygame.draw.rect(win,colour,rect)
    draw_text(win, text, (rect.x + 10, rect.y + 5))

class Button:
    def __init__(self, rect, text, colour, action=None):
        self.rect = pygame.Rect(rect)
        self.text = text 
        self.colour = colour
        self.action = action
        
    def draw(self, win):
        draw_button(win, self.rect, self.text, self.colour)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


stats=["Strength","Agility","Dexterity","Intellect", "Stamina", "Perception"]
def create_stat_buttons():
    return [
    {"name": stats[i], "value": 0, "rect": pygame.Rect(30, 30 + i * (STAT_BUTTON_HEIGHT + BUTTON_MARGIN), STAT_BUTTON_WIDTH, STAT_BUTTON_HEIGHT)}
    for i in range(len(stats))
    ]

ready_button = Button(pygame.Rect((width - READY_BUTTON_WIDTH) // 2, height - READY_BUTTON_HEIGHT - 20, READY_BUTTON_WIDTH, READY_BUTTON_HEIGHT), "Not Ready", READY_BUTTON_COLOUR_NOT_READY)

def draw_start_screen(win, stat_buttons, player):
    win.fill(START_BG_COLOUR)
    for button in stat_buttons:
        draw_button(win, button['rect'], f"{button['name']}: {button['value']}")
    draw_text(win, f"Stat Points: {player.stat_points}", (0, height - 40))
    ready_button.draw(win)
    pygame.display.update()

def handle_start_screen_events(stat_buttons, player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for button in stat_buttons:
                if button['rect'].collidepoint(pos) and player.stat_points > 0:
                    button['value'] += 1
                    player.stat_points -= 1
                    setattr(player, button['name'].lower()[:3], getattr(player, button['name'].lower()[:3]) + 1)

            if ready_button.is_clicked(pos) and player.stat_points == 0:
                ready_button.text = "Ready"
                ready_button.colour = READY_BUTTON_COLOUR
                player.ready = True
                return {"ready": True, "id": player.id, "stats":player.get_stats()}
    return None

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
        player_id=data['id'],
        stat_points=data.get('stat_points', 10),
        str=data.get('str', 0),
        agi=data.get('agi', 0),
        dex=data.get('dex', 0),
        int=data.get('int', 0),
        sta=data.get('sta', 0),
        per=data.get('per', 0),
        ready=data['ready']
    )
def dict_to_loot(data):
    """Convert a dictionary to a Loot object."""
    try:
        return loot(
            x=data['x'],
            y=data['y'],
            rarity=data['rarity'],
            colour=tuple(data['colour']),
            name=data['name'],
            item_value=data['item_value']
        )
    except KeyError as e:
        print(f"Missing key in loot data: {e}")
        raise

def update_players(player, players):
    players[player.id].x = player.x
    players[player.id].y = player.y
    players[player.id].colour = player.colour
    players[player.id].stat_points = player.stat_points
    players[player.id].str = player.str
    players[player.id].agi = player.agi
    players[player.id].dex = player.dex
    players[player.id].int = player.int
    players[player.id].sta = player.sta
    players[player.id].per = player.per
    players[player.id].ready = player.ready
    players[player.id].update()

def initialise_data(n):
    initial_data = n.getP()# player1_data should be a dictionary or a Player object

    if initial_data is None:
        print("Error: No initial data recieved.")
        return None, None, None
    
    player1_data = initial_data.get('player')
    loot_data = initial_data.get('loot')
    
    if player1_data is None or loot_data is None:
        print("Error: Initial data is not in expected format.")
        return None, None, None
    try:
        player1 = dict_to_player(player1_data)
    except KeyError as e:
        print(f"Error converting player1 data: {e}")
        return None, None, None
    
    players = {player1.id: player1}
    
    try:
        loot_items = [dict_to_loot(item) for item in loot_data]
    except KeyError as e:
        print(f"Error converting loot data: {e}")
        return None, None, None
    
    return players, loot_items, player1

def main():
    run = True
    n = Network()
    start_Screen = True
    stat_buttons = create_stat_buttons()
    both_ready = False
    players, loot_items, player1 = initialise_data(n)

    if players is None or loot_items is None or player1 is None:
        print("Error: Data cannot be initialised")
        return

    clock = pygame.time.Clock()
    

    # Initial screen for stat allocation and ready check
    while not both_ready:
        draw_start_screen(win, stat_buttons, player1)
        ready_data = handle_start_screen_events(stat_buttons, player1)

        if ready_data:
            try:
                # Send a ready signal to the server
                response = n.send(ready_data)
                print("Ready data sent, response: {response}")

                if response and response.get('both_ready', False):
                    both_ready = True
                    print("Both players are ready! Game will start soon.")    
                    # if data.get('game_state') == "started":
                    #     players_data = data.get('players', {})
                    #     for player_id, player_data in players_data.items():
                    #         if player_id not in players:
                    #             players[player_id] = dict_to_player(player_data)

            except Exception as e:
                print(f"Error while sending ready data: {e}")

    player = None
    game_started = False
    while run:
        clock.tick(120)
        try:

            data = n.send(player1)
            print(f"Recieved data from server: {data}")

            if data:
                game_state = data.get('game_state', 'waiting')
                if game_state == 'started' and not game_started:
                    print("Game has started!")
                    game_started = True
                elif game_state == 'waiting':
                    print(data.get('message', 'Waiting for players...'))


                players_data = data.get('players')
                loot_items_data = data.get('loot')
                
                if players_data is not None:
                    for player_id, player_data in players_data.items():
                        if player_id not in players:
                            players[player_id] = dict_to_player(player_data)
                        else:
                            try:
                                player = dict_to_player(player_data)
                                update_players(player, players)
                            except ValueError as e:
                                print(f"Error updating player ID: {player.id} data: {e}")
                else:
                    print("Warning: Received None for players_data") 
                                   
                if loot_items_data is not None:
                    loot_items = [dict_to_loot(item) for item in loot_items_data]
                else:
                    print(f"Warning: Recieved None for loot_items_data")

            else:
                if player:
                    print(f"Player data for id {player.id} is not  available")
            #    loot_items = [dict_to_loot(data) for data in loot_data]
                else:
                    print("No valid player data from the server")

        except Exception as e:
            print(f"Error recieving data from server: {e}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        player1.move()
        if game_started:
            redrawWindow(win, players, loot_items)
            
main()