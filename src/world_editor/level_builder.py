# Level Builder
# Author: Caleb, Matt
# Winter 2017

import pygame

from sprite_viewer import SpriteViewer
from main_game.camera import Camera
from main_game.world import World


class LevelBuilder:

    DISPLAY_WIDTH = 720
    DISPLAY_HEIGHT = 560
    SIDEBAR_WIDTH = 400
    TILE_WIDTH = 40

    selected_tile = None
    cam_width = DISPLAY_WIDTH / 2
    cam_height = DISPLAY_HEIGHT / 2
    SPRITE_WIDTH = 32
    CAMERA_SPEED = 5

    def __init__(self):
        pygame.init()

        self.window_width = LevelBuilder.DISPLAY_WIDTH + LevelBuilder.SIDEBAR_WIDTH
        self.window_height = LevelBuilder.DISPLAY_HEIGHT
        self.my_win = pygame.display.set_mode((self.window_width, self.window_height))

        self.spritesheet = pygame.image.load(
            "../assets/images/OtherSheet.png").convert_alpha()

        self.tile_width = 40
        self.world_width = 20
        self.world_height = 20
        self.world = World(self.world_width,
                           self.world_height,
                           self.spritesheet)

        self.sprite_width = LevelBuilder.SPRITE_WIDTH
        self.sprite_viewer = SpriteViewer(0,
                                          0,
                                          LevelBuilder.SIDEBAR_WIDTH,
                                          self.window_height,
                                          self.spritesheet,
                                          self.sprite_width)

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

    def click_tile(self, pos, is_foreground):
        adjusted_pos = (pos[0]-LevelBuilder.SIDEBAR_WIDTH, pos[1])
        x_scalar = LevelBuilder.DISPLAY_WIDTH / self.cam_width
        y_scalar = self.window_height / self.cam_height
        true_x = adjusted_pos[0]/x_scalar
        true_y = adjusted_pos[1]/y_scalar

        cam_x, cam_y = self.camera.get_location()[0], self.camera.get_location()[1]

        x_adj = true_x + cam_x % self.tile_width
        y_adj = true_y + cam_y % self.tile_width

        column = x_adj/self.tile_width
        row = y_adj/self.tile_width

        start_column = int(float(cam_x)/self.tile_width)
        start_row = int(float(cam_y)/self.tile_width)

        if is_foreground:
            tile = self.world.get_fg_tile(start_column + column, start_row + row)
            if tile is None:
                self.world.add_foreground_tile(start_column + column, start_row + row, self.sprite_viewer.get_rect())
            else:
                tile.change_sprite(self.sprite_viewer.get_rect())
        else:
            tile = self.world.get_bg_tile(start_column + column, start_row + row)
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
                    self.dx = -LevelBuilder.CAMERA_SPEED
                elif key_pressed == pygame.K_d:
                    self.dx = LevelBuilder.CAMERA_SPEED
                elif key_pressed == pygame.K_w:
                    self.dy = -LevelBuilder.CAMERA_SPEED
                elif key_pressed == pygame.K_s:
                    self.dy = LevelBuilder.CAMERA_SPEED
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

    def quit(self):
        pygame.quit()

    def export_level(self):
        name = raw_input("Please enter the filename to save: ")
        try:
            self.world.export_world("../assets/worlds/"+name+".json")
            print "Successfully saved "+name
        except IOError:
            print "Couldn't save world '"+name+"'"

    def import_level(self):
        name = raw_input("Please enter the filename to load: ")

        try:
            self.world.import_world("../assets/worlds/"+name+".json")
            print "Successfully loaded "+name
        except IOError:
            print "Couldn't load world '"+name+"'"

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

