# Player class, player objects can be NPCs or user controlled


class Player:

    def __init__(self, hp, energy, arm, str, dex, int, stam):
        self.hp = hp + 10*stam
        self.energy = energy
        self.arm = arm
        self.str = str
        self.dex = dex
        self.int = int
        self.stam = stam
