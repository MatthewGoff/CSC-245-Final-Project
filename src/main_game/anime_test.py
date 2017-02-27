# This is the test for animation
# @author Yunmeng Li
# @version Winter, 2017

import pygame
from main_game.animation import PlayerAnimation


class AnimeTest(object):

    DISPLAY_WIDTH = 300
    DISPLAY_HEIGHT = 300
    my_win = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    players = pygame.sprite.Group()

    @classmethod
    def init(cls):
        pygame.init()
        cls.player = PlayerAnimation(0, 0)
        cls.players.add(cls.player)

    @classmethod
    def handle_events(cls):

        keep_going = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False

            elif event.type == pygame.KEYDOWN:
                # Key pressed event
                key_pressed = chr(event.dict['key'] % 256)
                #print "Key pressed = %s" % key_pressed + "%d" % ord(key_pressed)

                if key_pressed == "s":
                    cls.player.face_moving()

                elif key_pressed == "w":
                    cls.player.back_moving()

                elif key_pressed == "a":
                    cls.player.left_moving()

                elif key_pressed == "d":
                    cls.player.right_moving()

            elif event.type == pygame.KEYUP:

                # Key released event
                key_released = chr(event.dict['key'] % 256)

                if key_released == "s":
                    cls.player.face_stop()

                elif key_released == "w":
                    cls.player.back_stop()

                elif key_released == "a":
                    cls.player.left_stop()

                elif key_released == "d":
                    cls.player.right_stop()

        return keep_going

    @classmethod
    def draw(cls):
        # Draw Background
        cls.my_win.fill(pygame.color.Color("LightGrey"))
        #pygame.draw.rect(cls.my_win,(165,165,165),())
        cls.players.draw(cls.my_win)
        # Swap display
        pygame.display.update()

    @classmethod
    def quit(cls):
        pygame.quit()

    @classmethod
    def run(cls):

        frame_rate = 240
        tick_time = int(1.0 / frame_rate * 1000)

        # The game loop starts here.
        keep_going = True
        while keep_going:

            #pygame.time.wait(tick_time)

            frame_rate = 240
            tick_time = int(1.0 / frame_rate * 1000)

            # The game loop starts here.
            keep_going = True
            while keep_going:
                keep_going = cls.handle_events()

                pygame.time.wait(tick_time)

                cls.draw()

            cls.quit()

        cls.quit()

AnimeTest.init()
AnimeTest.run()