# A main menu class
# Author: Matthew Goff
# Winter 2017

import pygame

from main_game.button import Button
from main_game.util import draw_text
from world_editor.level_builder import LevelBuilder
from main_game.campaign import Campaign
from main_game.credits import Credits

class MainMenu:
    WINDOW_SIZE = (600, 400)
    BUTTON_SIZE = (250, 50)
    ICON_SIZE = (256, 256)

    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode(MainMenu.WINDOW_SIZE)
        self.buttons = []

        rect = pygame.Rect(300,
                           120,
                           MainMenu.BUTTON_SIZE[0],
                           MainMenu.BUTTON_SIZE[1])
        self.buttons += [Button(rect.copy(),
                                40,
                                "Campaign",
                                self.campaign)]
        rect.top += 80
        self.buttons += [Button(rect.copy(),
                                40,
                                "World Editor",
                                self.editor)]
        rect.top += 80
        self.buttons += [Button(rect.copy(),
                                40,
                                "Credits",
                                self.credits)]

        self.icon = pygame.image.load("../assets/icon/icon_new2.png").convert_alpha()
        self.icon = pygame.transform.smoothscale(self.icon, MainMenu.ICON_SIZE)

        self.keep_going = False

    def campaign(self):
        self.keep_going = False
        pygame.quit()
        campaign = Campaign()
        campaign.run()

    def editor(self):
        self.keep_going = False
        pygame.quit()
        level_builder = LevelBuilder()
        level_builder.run()

    def credits(self):
        self.keep_going = False
        pygame.quit()
        credits = Credits()
        credits.run()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_going = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_pressed = event.dict['button']
                mouse_pos = event.dict['pos']

                if button_pressed == 1:
                    clicked_buttons = [button for button in self.buttons if
                                       button.rect.collidepoint(mouse_pos)]

                    if clicked_buttons:
                        clicked_buttons[0].action()

    def draw(self):
        self.window.fill(pygame.color.Color("LightGrey"))

        draw_text((MainMenu.WINDOW_SIZE[0]/2,
                   40),
                  "A Scheme to Adventure",
                  64,
                  self.window)

        draw_text((550, 387),
                  "Version 0.0.2",
                  20,
                  self.window)

        pygame.draw.line(self.window,
                         pygame.Color("black"),
                         (20, 70),
                         (MainMenu.WINDOW_SIZE[0]-20, 70),
                         3)

        self.window.blit(self.icon, (20, 85))
        for button in self.buttons:
            button.draw(self.window)

        pygame.display.update()

    def quit(self):
        pygame.quit()

    def run(self):

        frame_rate = 30
        tick_time = int(1.0 / frame_rate * 1000)

        # The game loop starts here.
        self.keep_going = True
        while self.keep_going:

            pygame.time.wait(tick_time)

            # 1. Handle events.
            self.handle_events()

            if self.keep_going:
                # 4. Draw frame
                self.draw()

        self.quit()