class Character:
    def __init__(self, name, attack):
        self.name = name
        self.attack = attack

    def attack(self, target):
        # Attack another character
        target.health -= self.attack