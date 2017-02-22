# Class runs the game loop for the campaign portion of the game.

# Level Builder
# Author: Caleb, Matt
# Winter 2017

import pygame

from camera import Camera
from world import World


class Campaign:

    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480

    def __init__(self):
        pygame.init()

        self.window_width = Campaign.WINDOW_WIDTH
        self.window_height = Campaign.WINDOW_HEIGHT
        self.my_win = pygame.display.set_mode((self.window_width, self.window_height))

        self.world_rows = 20
        self.world_columns = 20
        self.world = World.load("portal_forest")

        self.camera = Camera((200, 200),
                             self.cam_width,
                             self.cam_height,
                             self.world)
        self.camera_bounds = pygame.Rect(self.cam_width / 2,
                                         self.cam_height / 2,
                                         self.world.get_border().width - self.cam_width,
                                         self.world.get_border().height - self.cam_height)
        self.fullscreen = False
        self.dx = 0
        self.dy = 0

    def handle_events(self):

        keep_going = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False

            elif event.type == pygame.KEYDOWN:
                key_pressed = event.dict['key'] % 256
                if key_pressed == pygame.K_a:
                    self.dx = -LevelBuilder.camera_speed
                elif key_pressed == pygame.K_d:
                    self.dx = LevelBuilder.camera_speed
                elif key_pressed == pygame.K_w:
                    self.dy = -LevelBuilder.camera_speed
                elif key_pressed == pygame.K_s:
                    self.dy = LevelBuilder.camera_speed
                elif key_pressed == pygame.K_RETURN:
                    self.export_level()
                elif key_pressed == pygame.K_0:
                    self.import_level()
                elif key_pressed == pygame.K_ESCAPE:
                    if self.fullscreen:
                        pygame.display.set_mode((self.window_width,
                                                 self.window_height))
                        self.fullscreen = False
                    else:
                        pygame.display.set_mode((self.window_width,
                                                 self.window_height),
                                                pygame.FULLSCREEN)
                        self.fullscreen = True
            elif event.type == pygame.KEYUP:
                key_released = event.dict['key'] % 256
                if key_released == pygame.K_a or key_released == pygame.K_d:
                    self.dx = 0
                if key_released == pygame.K_s or key_released == pygame.K_w:
                    self.dy = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print "Button pressed:", event.dict['button'], "@", event.dict['pos']
                button_pressed = event.dict['button']
                target = event.dict['pos']

                if button_pressed == 1 and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    keep_going = self.click_tile(target, True)
                elif button_pressed == 1 and target[0] > LevelBuilder.SIDEBAR_WIDTH:  # Left click
                    keep_going = self.click_tile(target, False)
                elif button_pressed == 1 and target[0] <= LevelBuilder.SIDEBAR_WIDTH:
                    self.sprite_viewer.click_sprite(target)
                elif button_pressed == 5 and self.sprite_viewer.curr_row < (len(self.sprite_viewer.sprites))\
                        /self.sprite_viewer.sprites_per_row - self.sprite_viewer.num_rows:
                    self.sprite_viewer.curr_row += 1
                elif button_pressed == 4 and self.sprite_viewer.curr_row > 0:
                    self.sprite_viewer.curr_row -= 1

        return keep_going

    def apply_rules(self):
        next_pos = (self.camera.center[0]+self.dx,
                    self.camera.center[1]+self.dy)
        if self.camera_bounds.collidepoint(next_pos[0], next_pos[1]):
            self.camera.center = next_pos

    def draw(self):
        # Draw Background
        self.my_win.fill(pygame.color.Color("LightGrey"))

        # Draw cameras front to back
        self.camera.draw(LevelBuilder.SIDEBAR_WIDTH,
                         0,
                         LevelBuilder.DISPLAY_WIDTH,
                         self.window_height,
                         self.my_win)
        self.sprite_viewer.draw(self.my_win)

        # Swap display
        pygame.display.update()

    def simulate(self):
        pass

    def quit(self):
        pygame.quit()

    def export_level(self):
        self.world.export_world()

    def import_level(self):
        self.world.import_world()

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

