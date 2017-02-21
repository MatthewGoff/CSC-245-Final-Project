# A simple platforming game
# Author: Matthew Anderson
# Winter 2017

import json, math

import pygame

from world import World
from camera import Camera
from cursor import Cursor
from sprite_viewer import SpriteViewer
from tile import Tile


class LevelBuilder:

    width = 720
    height = 560
    sidebar_width = 400
    world_rows = 20
    world_columns = 20
    my_win = pygame.display.set_mode((width + sidebar_width, height))
    tile_width = 40
    selected_tile = None
    center = None
    world = None
    camera = None
    cam_width = width/2
    cam_height = height/2
    spritesheet = pygame.image.load("../images/OtherSheet.png").convert_alpha()
    sprite_width = 32
    camera_speed = 5

    def __init__(self):
        pygame.init()

        # The center of the camera
        self.center = Cursor(200, 200)

        # Size of the foreground camera viewport.
        width = self.cam_width
        height = self.cam_height

        self.world = World(self.world_columns, self.world_rows, self.tile_width, self.center, self.spritesheet, self.sprite_width)

        self.sprite_viewer = SpriteViewer(0,0, self.sidebar_width, self.height, self.spritesheet, self.sprite_width, self.tile_width)

        self.camera = Camera(self.center,width,height,self.world)
        self.camera_bounds = pygame.Rect(width / 2,
                                         height / 2,
                                         self.world.get_border().width - width,
                                         self.world.get_border().height - height)
        self.dx = 0
        self.dy = 0

    def click_tile(self, pos):
        adjusted_pos = (pos[0]-self.sidebar_width, pos[1])
        x_scalar = self.width/self.cam_width
        y_scalar = self.height/self.cam_height
        true_x = adjusted_pos[0]/x_scalar
        true_y = adjusted_pos[1]/y_scalar

        cam_x, cam_y = self.camera.get_location()[0], self.camera.get_location()[1]

        x_adj = true_x + cam_x % self.tile_width
        y_adj = true_y + cam_y % self.tile_width

        column = x_adj/self.tile_width
        row = y_adj/self.tile_width

        start_column = int(float(cam_x)/self.tile_width)
        start_row = int(float(cam_y)/self.tile_width)

        tile = self.world.get_tile(start_column + column, start_row + row)
        tile.change_sprite(self.sprite_viewer.get_rect())

        return True

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
                    keep_going = False
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
                if button_pressed == 1 and target[0] > self.sidebar_width:  # Left click
                    keep_going = self.click_tile(target)
                elif button_pressed == 1 and target[0] <= self.sidebar_width:
                    self.sprite_viewer.click_sprite(target)
                elif button_pressed == 5 and self.sprite_viewer.curr_row < len(self.sprite_viewer.sprites)-1:
                    self.sprite_viewer.curr_row += 1
                elif button_pressed == 4 and self.sprite_viewer.curr_row > 0:
                    self.sprite_viewer.curr_row -= 1

        return keep_going

    def apply_rules(cls):
        next_pos = (cls.center.pos[0]+cls.dx,
                    cls.center.pos[1]+cls.dy)
        if cls.camera_bounds.collidepoint(next_pos[0], next_pos[1]):
            cls.center.pos = next_pos

    def draw(self):
        # Draw Background
        self.my_win.fill(pygame.color.Color("LightGrey"))


        # Draw cameras front to back
        self.camera.draw(self.sidebar_width, 0, self.width, self.height, self.my_win)
        self.sprite_viewer.draw(self.my_win)

        # Swap display
        pygame.display.update()

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


level_builder = LevelBuilder()
level_builder.run()
