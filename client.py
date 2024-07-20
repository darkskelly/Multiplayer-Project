import pygame
from network import Network
from player import Player

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Penis")


def redrawWindow(win,player1, player2):
    win.fill((255,255,255))
    player1.draw(win)
    player2.draw(win)
    pygame.display.update()

def dict_to_player(data):
    """Convert a dictionary to a Player object."""
    return Player(
        x=data['x'],
        y=data['y'],
        width=data['width'],
        height=data['height'],
        colour=tuple(data['colour']),
        player_id=data['id']
    )


def main():
    run = True
    n = Network()
    player1_data = n.getP()# player1_data should be a dictionary or a Player object

    if player1_data is None:
        print("Error: No initial player data recieved.")
        return
    
    if isinstance(player1_data, dict):
        try:
            player1 = dict_to_player(player1_data)
            print(f"Player1 initialised: {player1_data}")
        except ValueError as e:
            print(f"Error converting player1 data: {e}")
            return
    else:
        print("Error: player1 data is not in expected format")
        return
    
    #initialises player_ids
    player2_id = 1 if player1.id == 0 else 0
    player2 = Player(0, 0, 50, 50, (0, 0, 255), player_id=player2_id)


    # Initialize player2 correctly based on player1's color
    if hasattr(player1, 'colour'):
        player1.id = 0 if player1.colour == (255,0,0) else 1
        player2 = Player(0, 0, 50, 50, (0, 0, 255), player_id=1 if player1.id == 0 else 0)
    else:
        print("Player1 doesn't have 'colour' attribute")

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        data = n.send(player1)
        print(f"Recieved data from server: {data}")

        if data:
            player2_data = data.get(player2.id)
            if player2_data:

                try:
                    # Update player2's attributes using dictionary keys
                    player2_data = dict_to_player(player2_data)
                    player2.x = player2_data.x
                    player2.y = player2_data.y
                    player2.colour = player2_data.colour
                    player2.update()
                except ValueError as e:
                    print(f"Error updating player2: {e}")
            else:
                print(f"Player2 data for id {player2.id} is not  available")
        else:
            print("No data recieved from server.")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        player1.move()
        redrawWindow(win , player1, player2)
main()