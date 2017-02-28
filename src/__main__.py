# Entrance point
# Author: Matthew Goff
# Winter 2017

from main_menu.main_menu import MainMenu


def main():
    '''mode = "campaign"

    if mode == "builder":
        level_builder = LevelBuilder()
        level_builder.run()
    elif mode == "campaign":
        campaign = Campaign()
        campaign.run()
    elif mode == "battle":
        demo()'''
    menu = MainMenu()
    menu.run()

if __name__ == "__main__":
    main()

