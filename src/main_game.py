# Entrance point
# Author: Matthew Goff
# Winter 2017

from world_editor.level_builder import LevelBuilder
from main_game.campaign import Campaign


if __name__ == "__main__":
    if False:
        level_builder = LevelBuilder()
        level_builder.run()
    else:
        campaign = Campaign()
        campaign.run()
