# Entrance point
# Author: Matthew Goff
# Winter 2017

from world_editor.level_builder import LevelBuilder
from main_game.campaign import Campaign
from main_game.battle import demo

if __name__ == "__main__":
    mode = "builder"

    if mode == "builder":
        level_builder = LevelBuilder()
        level_builder.run()
    elif mode == "campaign":
        campaign = Campaign()
        campaign.run()
    elif mode == "battle":
        demo()
