import pygame
from network import Network
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
        self.height = height
        self.colour = colour
        self.rect = (x,y,width,height)
        self.vel = 3
    def draw(self,win):
        pygame.draw.rect(win, self.colour, self.rect)
     
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= self.vel

        if keys[pygame.K_d]:
            self.x += self.vel

        if keys[pygame.K_w]:
            self.y -= self.vel

        if keys[pygame.K_s]:
            self.y += self.vel
        self.rect = (self.x,self.y,self.width, self.height)




def redrawWindow(win,p):
    win.fill((255,255,255))
    p.draw(win)
    pygame.display.update()

def main():
    run = True
    n = Network()
    startPos = n.getPos()   
    p = Player(50,50,100,100,(0,255,0))
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        p.move()
        redrawWindow(win , p)
main()