max_morale = 10
max_health = 10


class Player:

    def __init__(self, name):
        self.name = name
        self.morale = max_morale
        self.health = max_health
        self.weapon = []
        self.inventory = []
        self.alive = True
