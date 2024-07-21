

class loot:
    def __init__(self, x, y, rarity, colour):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.rarity = rarity
        self.colour = colour
        self.rect = (x, y, self.width, self.height)

    def draw(self, win):
        import pygame
        pygame.draw.rect(win, self.colour, self.rect)

# def generate_loot(map_width, map_height, num_items):
#     loot_items = []
#     for _ in range(num_items):
#         x = random.randint(0, map_width - 10)
#         y = random.randint(0, map_height - 10)
#         rarity = random.choice(['common', 'uncommon', 'rare', 'epic', 'legendary'])
#         colour = {
#             'common': (169, 169, 169),
#             'uncommon': (0, 255, 0),
#             'rare': (0, 0, 255),
#             'epic': (128, 0, 128),
#             'legendary': (255, 215, 0)
#         }[rarity]
#         loot_items.append(loot(x, y, rarity, colour))
#     return loot_items