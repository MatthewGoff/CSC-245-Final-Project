# A simple platforming game
# Author: Matthew Anderson
# Winter 2017

import pygame, math
from world import World
from camera import Camera
from cursor import Cursor
from sprite_viewer import SpriteViewer
from tile import Tile

class LevelBuilder:
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)

    width = 640
    height = 480
    sidebar_width = 200
    world_rows = 20
    world_columns = 20
    my_win = pygame.display.set_mode((width + sidebar_width, height))
    deltaIncrement = 40
    tile_width = 40
    selected_tile = None
    center = None
    world = None
    camera = None
    cam_width = 320
    cam_height = 240
    spritesheet = pygame.image.load("images/OtherSheet.png").convert_alpha()
    sprite_width = 32

    @classmethod
    def init(cls):
        pygame.init()

        # Create a player on left side of game.
        cls.center = Cursor(200, 200)

        # Size of the foreground camera viewport.
        width = cls.cam_width
        height = cls.cam_height

        cls.world = World(cls.world_columns, cls.world_rows, cls.tile_width, cls.center, cls.spritesheet, cls.sprite_width)

        cls.sprite_viewer = SpriteViewer(0,0, cls.sidebar_width, cls.height, cls.spritesheet, cls.sprite_width)

        # Make three cameras focused on player with increasingly large viewports of the three worlds.
        cls.camera = Camera(cls.center,width,height,cls.world)
        # Set initial change in x/y for the center to be zero
        cls.dx = 0
        cls.dy = 0

    @classmethod
    def click_tile(cls, pos):
        adjusted_pos = (pos[0]-cls.sidebar_width, pos[1])
        x_scalar = cls.width/cls.cam_width
        y_scalar = cls.height/cls.cam_height
        true_x = adjusted_pos[0]/x_scalar
        true_y = adjusted_pos[1]/y_scalar
        column = true_x/cls.tile_width
        row = true_y/cls.tile_width

        cam_pos = cls.camera.get_location()
        start_column = cam_pos[0]/cls.tile_width
        start_row = cam_pos[1]/cls.tile_width

        tile = cls.world.get_tile(start_column + column, start_row + row)
        tile.change_sprite(cls.sprite_viewer.get_sprite())

        return True









    @classmethod
    def handle_events(cls):

        keep_going = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False

            elif event.type == pygame.KEYDOWN:
                # Key pressed event
                key_pressed = chr(event.dict['key'] % 256)
                # print "Key pressed = %s" % key_pressed

                if key_pressed == "a":
                    new_x = cls.center.pos[0] - cls.deltaIncrement
                    if new_x > cls.camera.x_offset - cls.tile_width:
                        cls.center.pos = (new_x, cls.center.pos[1])

                elif key_pressed == "d":
                    new_x = cls.center.pos[0] + cls.deltaIncrement
                    if new_x < cls.world.width - cls.camera.x_offset + cls.tile_width:
                        cls.center.pos = (cls.center.pos[0] + cls.deltaIncrement, cls.center.pos[1])

                elif key_pressed == "w":
                    new_y = cls.center.pos[1] - cls.deltaIncrement
                    if new_y > cls.camera.y_offset - cls.tile_width:
                        cls.center.pos = (cls.center.pos[0], new_y)

                elif key_pressed == "s":
                    new_y = cls.center.pos[1] + cls.deltaIncrement
                    if new_y < cls.world.height - cls.camera.y_offset + cls.tile_width:
                        cls.center.pos = (cls.center.pos[0], cls.center.pos[1] + cls.deltaIncrement)

                elif pygame.K_ESCAPE:
                    cls.export_level()
                    keep_going = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print "Button pressed:", event.dict['button'], "@", event.dict['pos']
                button_pressed = event.dict['button']
                target = event.dict['pos']
                if button_pressed == 1 and target[0] > cls.sidebar_width:  # Left click
                    keep_going = cls.click_tile(target)
                elif button_pressed == 5 and cls.sprite_viewer.curr_index < len(cls.sprite_viewer.sprites)-1:
                    cls.sprite_viewer.curr_index += 1
                elif button_pressed == 4 and cls.sprite_viewer.curr_index > 0:
                    cls.sprite_viewer.curr_index -= 1

        return keep_going


    @classmethod
    def draw(cls):
        # Draw Background
        cls.my_win.fill(pygame.color.Color("LightGrey"))


        # Draw cameras front to back
        cls.camera.draw(cls.sidebar_width, 0, 640, 480, cls.my_win)
        cls.sprite_viewer.draw(cls.my_win)

        # Swap display
        pygame.display.update()

    @classmethod
    def quit(cls):
        pygame.quit()

    @classmethod
    def export_level(cls):
        cls.world.export_world()

    @classmethod
    def run(cls):

        frame_rate = 30
        tick_time = int(1.0 / frame_rate * 1000)

        # The game loop starts here.
        keep_going = True
        while keep_going:

            pygame.time.wait(tick_time)

            # 1. Handle events.
            keep_going = cls.handle_events()

            # 4. Draw frame
            cls.draw()

        cls.quit()



LevelBuilder.init()
LevelBuilder.run()
