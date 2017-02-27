# Class runs the game loop for the campaign portion of the game.

# Level Builder
# Author: Caleb, Matt
# Winter 2017

import pygame

from camera import Camera
from world import World
import constants


class Campaign:
    WINDOW_SIZE = (640, 480)
    CAMERA_SPEED = 10

    def __init__(self):
        pygame.init()

        self.fullscreen = False
        self.init_screen()
        self.world = World.load("portal_forest")
        self.init_camera()

        self.spritesheet = pygame.image.load(
            "../assets/images/OtherSheet.png").convert_alpha()

        self.dx = 0
        self.dy = 0

    def init_screen(self):
        if self.fullscreen:
            self.window_size = constants.NATIVE_SCREEN_SIZE
            pygame.display.set_mode(self.window_size,
                                    pygame.FULLSCREEN)
        else:
            self.window_size = Campaign.WINDOW_SIZE
            self.my_win = pygame.display.set_mode(self.window_size)

    def init_camera(self):
        self.camera = Camera((self.window_size[0]/2,
                              self.window_size[1]/2),
                             self.window_size[0],
                             self.window_size[1],
                             self.world)

    def handle_events(self):

        keep_going = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False

            elif event.type == pygame.KEYDOWN:
                key_pressed = event.dict['key'] % 256
                if key_pressed == pygame.K_a:
                    self.dx = -Campaign.CAMERA_SPEED
                elif key_pressed == pygame.K_d:
                    self.dx = Campaign.CAMERA_SPEED
                elif key_pressed == pygame.K_w:
                    self.dy = -Campaign.CAMERA_SPEED
                elif key_pressed == pygame.K_s:
                    self.dy = Campaign.CAMERA_SPEED
                elif key_pressed == pygame.K_ESCAPE:
                    if self.fullscreen:
                        self.fullscreen = False
                        self.init_screen()
                        self.init_camera()
                    else:
                        self.fullscreen = True
                        self.init_screen()
                        self.init_camera()
            elif event.type == pygame.KEYUP:
                key_released = event.dict['key'] % 256
                if key_released == pygame.K_a or key_released == pygame.K_d:
                    self.dx = 0
                if key_released == pygame.K_s or key_released == pygame.K_w:
                    self.dy = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_pressed = event.dict['button']

                if button_pressed == 5:
                    self.camera.zoom_out()

                elif button_pressed == 4:
                    self.camera.zoom_in()


        return keep_going

    def apply_rules(self):
        next_pos = (self.camera.center[0] + self.dx * self.camera.zoom,
                    self.camera.center[1] + self.dy * self.camera.zoom)
        self.camera.center = next_pos

    def draw(self):
        # Draw Background
        self.my_win.fill(pygame.color.Color("LightGrey"))

        # Draw cameras front to back
        self.camera.draw(0,
                         0,
                         self.window_size[0],
                         self.window_size[1],
                         self.my_win)

        # Swap display
        pygame.display.update()

    def quit(self):
        pygame.quit()

    def run(self):

        frame_rate = 30
        tick_time = int(1.0 / frame_rate * 1000)

        # The game loop starts here.
        keep_going = True
        while keep_going:
            pygame.time.wait(tick_time)

            # 1. Handle events.
            keep_going = self.handle_events()

            # 2. Apply rules
            self.apply_rules()

            # 4. Draw frame
            self.draw()

        self.quit()