# Doors are tiles that act as portals between worlds.
# Author Caleb
# Version Winter 2017

import pygame
import constants
from tile import Tile


class Door(Tile):
    def __init__(self, spritesheet, sprite_loc, world_coords, dest_world, dest_coords):
        Tile.__init__(self, spritesheet, sprite_loc, world_coords)
        self.dest_world = None
        self.dest_coords = None
        self.dest_world = dest_world
        self.dest_coords = dest_coords

        width = constants.TILE_WIDTH
        door_overlay = pygame.image.load(constants.DOOR_OVERLAY_PATH).convert_alpha()
        self.door_overlay = pygame.transform.smoothscale(door_overlay, (width, width))
        self.alt_img = self.image.copy()
        self.alt_img.blit(self.door_overlay, (0,0))

    def to_json(self):
        return {
            "world_loc": self.world_loc,
            "sprite_loc": self.sprite_loc,
            "flipped": self.sprite_flipped,
            "passable": self.passable,
            "dest_world": self.dest_world,
            "dest_x": self.dest_coords[0],
            "dest_y": self.dest_coords[1]
        }

    def change_sprite(self, rect):
        self.sprite_loc = [rect.left, rect.top]
        image = self.spritesheet.subsurface(rect).copy()
        self.image = pygame.transform.smoothscale(image, (self.width, self.width))
        self.alt_img = pygame.transform.smoothscale(image, (self.width, self.width))
        self.alt_img.blit(self.door_overlay, (0, 0))

