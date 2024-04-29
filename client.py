import pygame
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Clit")

clientNumber = 0

class Player():
    def __init__(self,x,y,width,height,colour):
        self.x = x
        self.y = y
        self.width = width
        self.colour = colour
        self.rect = (x,y,width,height)
    def draw(self,win):
        pygame.draw.rect(win, self.colour, self.rect)
    
    def move(self):
    pygame.key.get_pressed()


def redrawWindow():
    win.fill((255,255,255))
    pygame.display.update()

def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        redrawWindow()