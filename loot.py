class loot:
    def __init__(self, x, y, rarity, colour, name, item_value):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.rarity = rarity
        self.colour = colour
        self.rect = (x, y, self.width, self.height)
        self.item_value = item_value
        self.name = name

    def draw(self, win):
        import pygame
        pygame.draw.rect(win, self.colour, self.rect)

class Weapon(loot):
    def __init__(self, x, y, rarity, colour, name, item_value, damage):
        super().__init__(x, y, rarity, colour, name, item_value)
        self.damage = damage

    def __repr__(self):
        return f"Weapon({self.name}, Damage: {self.damage}, Rarity: {self.rarity}, Value: {self.item_value})"

