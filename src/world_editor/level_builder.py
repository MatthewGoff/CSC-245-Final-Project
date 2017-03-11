# A graphical world map editor
# Author: Caleb, Matt
# Winter 2017

import pygame, json

import main_game.prompt
from sprite_viewer import SpriteViewer
from main_game.camera import UnboundCamera
from main_game.world import World
from main_game.button import Button
from main_game.door import Door
from main_game.tile import Tile


class LevelBuilder:

    DISPLAY_WIDTH = 720
    DISPLAY_HEIGHT = 560
    # Width of the sprite browser
    SIDEBAR_WIDTH = 400
    # Speed of panning
    CAMERA_SPEED = 10
    # File path to the sprite sheet
    SPRITESHEET_PATH = "../assets/images/TheSheet.png"

    def __init__(self):
        pygame.init()
        # Initialize window
        self.window_width = LevelBuilder.DISPLAY_WIDTH + LevelBuilder.SIDEBAR_WIDTH
        self.window_height = LevelBuilder.DISPLAY_HEIGHT
        self.my_win = pygame.display.set_mode((self.window_width, self.window_height))
        # Initialize sprite sheet
        self.spritesheet = pygame.image.load(
            LevelBuilder.SPRITESHEET_PATH).convert_alpha()
        # Initialize world
        #self.tile_width = 40
        self.world_width = 20
        self.world_height = 20
        self.world = World(self.world_width,
                           self.world_height,
                           self.spritesheet)
        # Initialize sidebar sprite browser
        self.sprite_viewer = SpriteViewer(0,
                                          0,
                                          LevelBuilder.SIDEBAR_WIDTH,
                                          self.window_height,
                                          self.spritesheet)

        self.selected_tile = None
        # Initialize camera
        self.cam_width = LevelBuilder.DISPLAY_WIDTH
        self.cam_height = LevelBuilder.DISPLAY_HEIGHT
        self.camera = UnboundCamera((400, 400),
                                    LevelBuilder.DISPLAY_WIDTH,
                                    LevelBuilder.DISPLAY_HEIGHT,
                                    self.world)
        self.fullscreen = False
        self.dx = 0
        self.dy = 0

        self.prompt = None
        self.in_prompt = False

    # Place the correct sprite on the clicked tile
    def click_tile(self, loc, is_foreground):

        if is_foreground:
            tile = self.world.foreground_tiles[loc[0]][loc[1]]
            # If no foreground tile exists for that location, create one
            if tile is None:
                self.world.add_foreground_tile(loc[0], loc[1], self.sprite_viewer.get_rect())
                tile = self.world.foreground_tiles[loc[0]][loc[1]]
                if not tile.passable:
                    tile.swap_image()
            else:
                tile.change_sprite(self.sprite_viewer.get_rect())
                if not tile.passable:
                    tile.swap_image()
        else:
            tile = self.world.get_bg_tile(loc[0], loc[1])
            tile.change_sprite(self.sprite_viewer.get_rect())
            if not tile.passable:
                tile.swap_image()
        # If the user has flipped the sprite horizontally, flip the tile's sprite
        if self.sprite_viewer.sprite_flipped:
            tile.image = pygame.transform.flip(tile.image, True, False)
            tile.alt_img = pygame.transform.flip(tile.alt_img, True, False)
            tile.sprite_flipped = True

        return True

    def toggle_tile_passability(self, loc, is_foreground):
        if is_foreground:
            tile = self.world.foreground_tiles[loc[0]][loc[1]]
        else:
            tile = self.world.get_bg_tile(loc[0], loc[1])
        if tile is not None and not isinstance(tile, Door):
            if tile.passable:
                tile.passable = False
            else:
                tile.passable = True
            tile.swap_image()
        return True

    def toggle_door(self, loc, is_foreground):
        if is_foreground:
            tile = self.world.foreground_tiles[loc[0]][loc[1]]
        else:
            tile = self.world.get_bg_tile(loc[0], loc[1])
        if tile is not None and tile.passable:
            if isinstance(tile, Door):
                self.world.replace_door_with_tile(tile.world_loc[0], tile.world_loc[1], is_foreground)
            else:
                self.prompt = main_game.prompt.door_placement(self.my_win.get_width(),
                                                              self.my_win.get_height(),
                                                              loc, is_foreground)
                self.in_prompt = True
        return True

    # Process user input
    def handle_events(self):

        keep_going = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
            elif self.in_prompt:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_pressed = event.dict['button']
                    mouse_pos = event.dict['pos']
                    clicked_obj = self.prompt.check_collisions(mouse_pos)
                    if button_pressed == 1:
                        if isinstance(clicked_obj, Button):
                            if clicked_obj.action is "okay":
                                self.in_prompt = False
                            elif clicked_obj.action is "exit":
                                keep_going = False
                            elif clicked_obj.action is "door":
                                self.world.replace_tile_with_door(self.prompt.output_dict["column"],
                                                                  self.prompt.output_dict["row"],
                                                                  self.prompt.output_dict["fg"],
                                                                  self.prompt.output_dict["world"],
                                                                  (self.prompt.output_dict["x"],
                                                                   self.prompt.output_dict["y"]))
                                self.in_prompt = False
                elif event.type == pygame.KEYDOWN:
                    key_pressed = event.dict['key'] % 256
                    self.prompt.handle_keydown(key_pressed)
            elif event.type == pygame.KEYDOWN:
                key_pressed = event.dict['key'] % 256
                # WASD keys pan the camera
                if key_pressed == pygame.K_a:
                    self.dx = -LevelBuilder.CAMERA_SPEED
                elif key_pressed == pygame.K_d:
                    self.dx = LevelBuilder.CAMERA_SPEED
                elif key_pressed == pygame.K_w:
                    self.dy = -LevelBuilder.CAMERA_SPEED
                elif key_pressed == pygame.K_s:
                    self.dy = LevelBuilder.CAMERA_SPEED
                # ENTER/RETURN saves the level
                elif key_pressed == pygame.K_RETURN:
                    self.export_level()
                # 0 loads a saved level
                elif key_pressed == pygame.K_0:
                    self.import_level()
                # Space mirrors the sprite horizontally
                elif key_pressed == pygame.K_SPACE:
                    curr_sprite = self.sprite_viewer.selected_sprite
                    if self.sprite_viewer.sprite_flipped:
                        self.sprite_viewer.sprite_flipped = False
                    else:
                        self.sprite_viewer.sprite_flipped = True
                    self.sprite_viewer.selected_sprite = pygame.transform.flip(curr_sprite, True, False)
                # ESC toggles fullscreen
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
                # Stop moving the camera
                if key_released == pygame.K_a or key_released == pygame.K_d:
                    self.dx = 0
                if key_released == pygame.K_s or key_released == pygame.K_w:
                    self.dy = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_pressed = event.dict['button']
                mouse_pos = event.dict['pos']
                # Check if the mouse is in the world area (as opposed to the browser area)
                if mouse_pos[0] > LevelBuilder.SIDEBAR_WIDTH:

                    if button_pressed == 1 or button_pressed == 3:
                        camera_pos = (mouse_pos[0] - LevelBuilder.SIDEBAR_WIDTH,
                                      mouse_pos[1])
                        world_pos = self.camera.get_click_location(camera_pos)

                        clicked_tiles = [tile for tile in self.world.bg_sprites
                                         if
                                         tile.rect.collidepoint(world_pos)]

                        if clicked_tiles:
                            click_loc = clicked_tiles[0].world_loc
                            if button_pressed == 1:
                                # Apply selected sprite to background tile
                                is_foreground = False
                            elif button_pressed == 3:
                                # Apply selected sprite to foreground tile
                                is_foreground = True
                            # Toggle tile passability
                            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                                keep_going = self.toggle_tile_passability(click_loc, is_foreground)
                            elif pygame.key.get_mods() & pygame.KMOD_ALT:
                                keep_going = self.toggle_door(click_loc, is_foreground)
                            else:
                                keep_going = self.click_tile(click_loc, is_foreground)
                    # Scroll wheel/ball zooms the camera
                    elif button_pressed == 5:
                        self.camera.zoom_out()
                    elif button_pressed == 4:
                        self.camera.zoom_in()
                # If the mouse is in the sprite browser area
                else:
                    if button_pressed == 1:
                        # Select the clicked sprite
                        self.sprite_viewer.click_sprite(mouse_pos)
                    # Scroll wheel/ball scrolls through the sprites in the browser
                    elif button_pressed == 5 and self.sprite_viewer.curr_row < (
                            len(
                                self.sprite_viewer.sprites)) \
                            / self.sprite_viewer.sprites_per_row - self.sprite_viewer.num_rows:
                        self.sprite_viewer.curr_row += 1
                    elif button_pressed == 4 and self.sprite_viewer.curr_row > 0:
                        self.sprite_viewer.curr_row -= 1

        return keep_going

    # Update the camera center to appropriately reflect its movement
    def apply_rules(self):
        next_pos = (self.camera.center[0] + self.dx * self.camera.zoom,
                    self.camera.center[1] + self.dy * self.camera.zoom)
        self.camera.center = next_pos

    def draw(self):
        # Draw Background
        self.my_win.fill(pygame.color.Color("LightGrey"))
        # Draw camera
        self.camera.draw(LevelBuilder.SIDEBAR_WIDTH,
                         0,
                         LevelBuilder.DISPLAY_WIDTH,
                         LevelBuilder.DISPLAY_HEIGHT,
                         self.my_win)
        # Draw sprite browser sidebar
        self.sprite_viewer.draw(self.my_win)

        if self.in_prompt:
            self.prompt.draw(self.my_win)
        # Swap display
        pygame.display.update()

    def quit(self):
        pygame.quit()

    # Save the world as a json file
    def export_level(self):
        name = raw_input("Please enter the filename to save: ")
        try:
            self.world.export_world("../assets/worlds/"+name+".json")
            print "Successfully saved "+name
        except IOError:
            print "Couldn't save world '"+name+"'"

    # Load a saved world
    def import_level(self):
        name = raw_input("Please enter the filename to load: ")

        try:
            data = json.load(open("../assets/worlds/"+name+".json"))
            self.world = World(data["width = "],
                           data["height = "],
                           self.spritesheet)
            self.camera = UnboundCamera((400, 400),
                                 LevelBuilder.DISPLAY_WIDTH,
                                 LevelBuilder.DISPLAY_HEIGHT,
                                 self.world)
            self.world.import_world("../assets/worlds/"+name+".json")
            print "Successfully loaded "+name
            for row in self.world.foreground_tiles:
                for tile in row:
                    if tile is not None and not tile.passable:
                        tile.swap_image()
            for row in self.world.background_tiles:
                for tile in row:
                    if not tile.passable:
                        tile.swap_image()
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

