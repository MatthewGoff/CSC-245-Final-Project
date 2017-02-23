# Entrance point
# Author: Matthew Goff
# Winter 2017

from world_editor.level_builder import LevelBuilder
# Uncomment below to run the battle demo
#from main_game.battle import Battle


if __name__ == "__main__":
    level_builder = LevelBuilder()
    level_builder.run()