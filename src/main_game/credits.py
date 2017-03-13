# Credits
# Caleb
# Winter 2017

import pygame
import __main__

class Credits:
    def __init__(self):
        pygame.init()
        self.window_size = (640, 480)
        self.window = pygame.display.set_mode(self.window_size)

        font = pygame.font.SysFont("monospace", 12)
        msg = "Caleb Seymour"
        msg1 = font.render(msg, True, pygame.color.Color("black"))
        msg = "Matthew Goff"
        msg2 = font.render(msg, True, pygame.color.Color("black"))
        msg = "Monica Li"
        msg3 = font.render(msg, True, pygame.color.Color("black"))
        msg = "Josh Wasserman"
        msg4 = font.render(msg, True, pygame.color.Color("black"))


        self.window.fill(pygame.color.Color("white"))
        self.window.blit(msg1, (0, 0))
        self.window.blit(msg2, (0, 14))
        self.window.blit(msg3, (0, 28))
        self.window.blit(msg4, (0, 42))
        pygame.display.update()

    def run(self):
        frame_rate = 30
        tick_time = int(1.0 / frame_rate * 1000)

        # The game loop starts here.
        keep_going = True
        while keep_going:
            pygame.time.wait(tick_time)

            keep_going = self.handle_events()

        __main__.main()
        self.quit()

    def handle_events(self):
        keep_going = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
        return keep_going

    def quit(self):
        pygame.quit()