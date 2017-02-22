# Class runs the game loop for Battle portion of the game

class Battle:

    def __init__(self, party1, party2, pos):
        self.location = pos
        self.party1 = party1
        self.party2 = party2
        self.friendlies = party1.members
        self.enemies = party2.members

