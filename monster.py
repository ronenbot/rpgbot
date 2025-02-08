import random
class Monster:

    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

    def spawn(self):
        # Spawn a new monster
        self.name = random.choice(["goblin", "orc", "skeleton"])
        return self.name

# premade monsters
goblin = Monster("Goblin", 10, 2, 1)
orc = Monster("Orc", 15, 3, 2)
skeleton = Monster("Skeleton", 5, 1, 0)

