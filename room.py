import random
class Room:
    def __init__(self):
        self.template =None
        self.description = ""
        self.creatures = []
        self.objects = []
        self.features = []

    def generate(self):
        # Randomly select a room template
        self.template = "monster"
        #self.template = random.choice(["empty", "treasure", "monster", "puzzle"])

        if self.template == "empty":
            self.description = "You find yourself in an empty room."
        elif self.template == "treasure":
            self.description = "You find a chest filled with treasure!"
            self.objects.append("chest")
        elif self.template == "monster":
            self.description = "You find a fearsome monster waiting for you!"
            self.creatures.append("goblin")
        elif self.template == "puzzle":
            self.description = "You find a mysterious puzzle that needs to be solved."
            self.features.append("puzzle")

