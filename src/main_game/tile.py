#
# Author: Caleb, Matt
# Winter 2017

import pygame

import constants


class Tile(pygame.sprite.Sprite):
    def __init__(self, spritesheet, sprite_loc, world_coords):
        pygame.sprite.Sprite.__init__(self)

        x = world_coords[0] * constants.TILE_WIDTH
        y = world_coords[1] * constants.TILE_WIDTH
        width = constants.TILE_WIDTH
        self.rect = pygame.Rect(x, y, width, width)

        self.world_loc = world_coords
        self.x = x
        self.y = y
        self.width = width
        self.spritesheet = spritesheet
        self.sprite_loc = sprite_loc
        self.spriteWidth = width
        rect = pygame.Rect(sprite_loc[0], sprite_loc[1], self.spriteWidth, self.spriteWidth)
        image = spritesheet.subsurface(rect).copy()
        self.image = pygame.transform.smoothscale(image, (width, width))
        self.sprite_flipped = False

    def to_json(self):
        return {
            "world_loc": self.world_loc,
            "sprite_loc": self.sprite_loc,
            "flipped": self.sprite_flipped
        }

    def __str__(self):
        return "sprite at position " + str(self.sprite_loc) + " at (" + str(self.x) + ", " + str(self.y) + ")"

    def draw(self, window):
            window.blit(self.image, (self.x, self.y))

    def change_sprite2(self, sprite):
        self.image = pygame.transform.smoothscale(sprite, (self.width, self.width))

    def change_sprite(self, rect):
        self.sprite_loc = [rect.left, rect.top]
        image = self.spritesheet.subsurface(rect).copy()
        self.image = pygame.transform.smoothscale(image, (self.width, self.width))