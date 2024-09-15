import pygame

class Player():
    def __init__(self,x,y,width,height,colour, player_id=0, inventory = {}):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.id = player_id
        self.rect = (x,y,width,height)
        self.vel = 3
        self.inventory = inventory #Functionality requried for if a player loads in with items in inv
        

    def draw(self,win):
        pygame.draw.rect(win, self.colour, self.rect)
     
    def move(self):
        keys = pygame.key.get_pressed()
        # for other_player in players.value():
        #     if other_player.id != self.id:
        #         self.handle_collision(other_player, keys)

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

    def check_collision(self, other_player):
        """Check if the player collides with another player."""
        if (self.x < other_player.x + other_player.width and
            self.x + self.width > other_player.x and
            self.y < other_player.y + other_player.height and
            self.y + self.height > other_player.y):
            return True
        return False

    def handle_collision(self, other_player, keys):
        """Handle the movement restrictions due to collision."""
        if self.check_collision(other_player):
            if keys[pygame.K_a] and self.x > other_player.x:
                self.x += self.vel
            if keys[pygame.K_d] and self.x < other_player.x:
                self.x -= self.vel
            if keys[pygame.K_w] and self.y > other_player.y:
                self.y += self.vel
            if keys[pygame.K_s] and self.y < other_player.y:
                self.y -= self.vel