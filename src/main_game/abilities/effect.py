# Interface for effects
# Caleb
# Winter 2017

class Effect:

    def __init__(self):
        self.start = None
        self.end = None
        self.target = None
        self.duration = None

    def affect_targets(self, round):
        pass