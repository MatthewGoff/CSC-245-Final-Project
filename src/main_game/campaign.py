# Class runs the game loop for the campaign portion of the game.

import pygame

class Campaign(object):

    def __init__(self):
        pass

    def handle_events(self):
        pass

    def simulate(self):
        pass

    def draw(self):
        pass

    def quit(self):
        pygame.quit()

    def run(self):
        frame_rate = 60
        tick_time = int(1.0 / frame_rate * 1000)

        # The game loop starts here.

        running = True
        while running:
            pygame.time.wait(tick_time)

            # 1. Handle events.
            running = self.handle_events()

            # 4. Draw frame
            self.draw()

        self.quit()
