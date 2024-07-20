import random

class loot:
    RARITY_LEVELS = { #Change to hex code
        'common': 'green',
        'uncommon': 'blue',
        'rare': 'purple',
        'legendary': 'orange'
    }

    def __init__(self, rarity):
        if rarity not in Loot.RARITY_LEVELS:
            raise ValueError("Invalid rarity level")
        self.rarity = rarity
        self.color = Loot.RARITY_LEVELS[rarity]

    @staticmethod
    def generate_random_loot():
        roll = random.randint(1, 100)
        if roll <= 50:
            return Loot('common')
        elif roll <= 80:
            return Loot('uncommon')
        elif roll <= 95:
            return Loot('rare')
        else:
            return Loot('legendary')

    def __repr__(self):
        return f"Loot(rarity={self.rarity}, color={self.color})"
