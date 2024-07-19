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

def main():
    run = True
    n = Network()
    player1 = n.getP()
   

    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        player2 = n.send(player1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        player1.move()
        redrawWindow(win , player1, player2)
main()