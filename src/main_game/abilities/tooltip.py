# A mouseover ability tooltip
# Author Caleb
# Winter 2017

from main_game.prompt import Prompt

class Tooltip(Prompt):
    def __init__(self, ability, cost, description):
        Prompt.__init__(self, 220, 220, 200, 200, "Blue")
        self.add_text(ability, "freesansbold.ttf", 30, True, "White")
        self.v_space(20)
        self.add_text("Cost: " + cost, "freesansbold.ttf", 25, False, "White")
        self.v_space(20)
        self.add_text(description, "freesansbold.ttf", 25, False, "White")
