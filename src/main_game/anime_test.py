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

    # Instead of boolean, int is used here to determine which direction
    # is the player moving to.
    # 0 - stop
    # 1 - 's', move down; 2 - 'w', move up
    # 3 - 'a', move left; 4 - 'd', move right
    direction = 0

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
                    cls.direction = 1

                elif key_pressed == "w":
                    cls.direction = 2

                elif key_pressed == "a":
                    cls.direction = 3

                elif key_pressed == "d":
                    cls.direction = 4

            elif event.type == pygame.KEYUP:

                # Key released event
                key_released = chr(event.dict['key'] % 256)

                if key_released == "s":
                    cls.direction = 0
                    cls.player.face_stop()

                elif key_released == "w":
                    cls.direction = 0
                    cls.player.back_stop()

                elif key_released == "a":
                    cls.direction = 0
                    cls.player.left_stop()

                elif key_released == "d":
                    cls.direction = 0
                    cls.player.right_stop()

        return keep_going

    @classmethod
    def apply_animation(cls):
        # Checks the direction, and call the animation function to update imgs

            if cls.direction == 1:  # 's', move down
                cls.player.face_moving()
                cls.player.walk(0, cls.player.speed)
            elif cls.direction == 2:  # 'w', move up
                cls.player.back_moving()
                cls.player.walk(0, -cls.player.speed)
            elif cls.direction == 3:  # 'a', move left
                cls.player.left_moving()
                cls.player.walk(-cls.player.speed, 0)
            elif cls.direction == 4:  # 'd', move right
                cls.player.right_moving()
                cls.player.walk(cls.player.speed, 0)

    @classmethod
    def draw(cls):
        # Draw Background
        cls.my_win.fill(pygame.color.Color("LightGrey"))
        cls.players.draw(cls.my_win)
        # Swap display
        pygame.display.update()

    @classmethod
    def quit(cls):
        pygame.quit()

    @classmethod
    def run(cls):

        frame_rate = 30
        tick_time = int(1.0 / frame_rate * 1000)
        # Current frame - the current number of frame, also means how many
        #           frames have passed.
        current_frame = 0
        # Animation frame - how many frames should passed before switching
        #           to next animation
        animation_frame = frame_rate / 10

        # The game loop starts here.
        keep_going = True
        while keep_going:

            # Keeps track of frames since last image was changed
            current_frame += 1

            keep_going = cls.handle_events()

            # Changes images when it's time to change
            if current_frame > animation_frame:
                cls.apply_animation()
                # Resets tracking frame to zero again to restart
                # a new checking progress
                current_frame = 0

            pygame.time.wait(tick_time)

            cls.draw()

        cls.quit()

AnimeTest.init()
AnimeTest.run()