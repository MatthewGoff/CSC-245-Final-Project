# Class runs the game loop for the campaign portion of the game.
# Author: Caleb, Matt
# Winter 2017

import pygame

from camera import BoundCamera
from world import World
from party import Party
from battle import demo
from button import Button
from util import Vec2D
import constants
from prompt import campaign_start, death, battle_won, input_example


class Campaign:
    WINDOW_SIZE = (640, 480)
    USER_SPEED = 5

    def __init__(self):
        pygame.init()

        self.fullscreen = True
        self.init_screen()
        self.world = World.load("door_demo1")
        enemy_image = pygame.image.load("../assets/images/OtherSheet.png").convert_alpha()
        enemy_rect = pygame.Rect(2016, 224, 32, 32)
        enemy_image = enemy_image.subsurface(enemy_rect).copy()
        enemy = Party((52, 460),
                      32,
                      (32, 32),
                      enemy_image,
                      self.world,
                      self.battle)
        self.world.add_party(enemy)

        player_image = pygame.image.load("../assets/images/player.png").convert_alpha()
        player_rect = pygame.Rect(0, 0, 48, 48)
        player_image = player_image.subsurface(player_rect).copy()
        self.user = Party(self.world.get_border().center,
                          32,
                          (10,10),
                          player_image,
                          self.world,
                          self.battle)
        self.world.add_party(self.user)
        self.init_camera()

        self.spritesheet = pygame.image.load(
            "../assets/images/TheSheet.png").convert_alpha()

        self.dx = 0
        self.dy = 0

        self.camera.set_zoom(.4)

        self.prompt = campaign_start((self.my_win.get_width(), self.my_win.get_height()))
        self.in_prompt = True

    def init_screen(self):
        if self.fullscreen:
            self.window_size = constants.NATIVE_SCREEN_SIZE
            self.my_win = pygame.display.set_mode(self.window_size,
                                                  pygame.FULLSCREEN)
        else:
            self.window_size = Campaign.WINDOW_SIZE
            self.my_win = pygame.display.set_mode(self.window_size)

    def init_camera(self):
        self.camera = BoundCamera(self.user,
                                  self.window_size[0],
                                  self.window_size[1],
                                  self.world)
        self.camera.set_zoom(.3)

    def change_world(self, world, party_coords):
        self.world = World.load(world)
        self.user.world = self.world
        self.user.set_pos(party_coords)
        self.world.add_party(self.user)
        self.init_camera()

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
                elif event.type == pygame.KEYDOWN:
                    key_pressed = event.dict['key'] % 256
                    self.prompt.handle_keydown(key_pressed)

            elif event.type == pygame.KEYDOWN:
                key_pressed = event.dict['key'] % 256
                print chr(key_pressed)
                if key_pressed == pygame.K_a:
                    self.dx += -Campaign.USER_SPEED
                elif key_pressed == pygame.K_d:
                    self.dx += Campaign.USER_SPEED
                elif key_pressed == pygame.K_w:
                    self.dy += -Campaign.USER_SPEED
                elif key_pressed == pygame.K_s:
                    self.dy += Campaign.USER_SPEED
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
                if key_released == pygame.K_a:
                    self.dx -= -Campaign.USER_SPEED
                elif key_released == pygame.K_d:
                    self.dx -= Campaign.USER_SPEED
                elif key_released == pygame.K_w:
                    self.dy -= -Campaign.USER_SPEED
                elif key_released == pygame.K_s:
                    self.dy -= Campaign.USER_SPEED
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_pressed = event.dict['button']

                if button_pressed == 5:
                    self.camera.zoom_out()

                elif button_pressed == 4:
                    self.camera.zoom_in()

        return keep_going

    def apply_rules(self):
        self.user.set_velocity(self.dx, self.dy)

    def simulate(self):
        door = self.world.simulate()
        if door is not None:
            self.change_world(door.dest_world, door.dest_coords)

    def draw(self):
        # Draw Background
        self.my_win.fill(pygame.color.Color("LightGrey"))

        # Draw cameras front to back
        self.camera.draw(0,
                         0,
                         self.window_size[0],
                         self.window_size[1],
                         self.my_win)
        if self.in_prompt:
            self.prompt.draw(self.my_win)

        # Swap display
        pygame.display.update()

    def battle(self, enemy):
        # A battle between the plyer and the enemy party needs resolving
        if enemy != self.user:
            self.dx = 0
            self.dy = 0
            if demo(self.my_win):
                self.world.remove_party(enemy)
                self.prompt = battle_won((self.my_win.get_width(), self.my_win.get_height()))
                self.in_prompt = True
            else:
                self.world.remove_party(self.user)
                self.prompt = death((self.my_win.get_width(), self.my_win.get_height()))
                self.in_prompt = True

        self.init_screen()
        self.init_camera()

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

            # 3. Simulate
            self.simulate()

            # 4. Draw frame
            self.draw()

        self.quit()