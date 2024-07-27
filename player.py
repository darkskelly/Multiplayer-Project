import pygame

class Player():
    def __init__(self,x,y,width,height,colour, player_id=0,stat_points=10, str=0, agi=0, dex=0, int=0, sta=0, per=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.id = player_id
        self.rect = (x,y,width,height)
        self.vel = 3
        self.stat_points = stat_points
        self.str = str
        self.agi = agi
        self.dex = dex
        self.int = int
        self.sta = sta
        self.per = per
        

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
        
        self.update()
    
    def update(self):
        self.rect = (self.x,self.y,self.width, self.height)
        
    def get_stats(self):
        return {
            "str": self.str,
            "agi": self.agi,
            "dex": self.dex,
            "int": self.int,
            "sta": self.sta,
            "per": self.per
        }