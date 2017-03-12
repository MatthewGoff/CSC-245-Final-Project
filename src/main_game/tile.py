# Worlds are made up of tiles
# Author: Caleb, Matt
# Winter 2017

import pygame
import constants


class Tile(pygame.sprite.Sprite):
    def __init__(self, spritesheet, sprite_loc, world_coords):
        pygame.sprite.Sprite.__init__(self)

        x = world_coords[0] * constants.TILE_WIDTH
        y = world_coords[1] * constants.TILE_WIDTH
        # tile position
        self.world_loc = world_coords
        # pixel position
        self.x = x
        self.y = y

        width = constants.TILE_WIDTH
        self.width = width

        self.rect = pygame.Rect(x, y, width, width)
        self.spritesheet = spritesheet
        self.sprite_loc = sprite_loc
        self.spriteWidth = width
        rect = pygame.Rect(sprite_loc[0], sprite_loc[1], self.spriteWidth, self.spriteWidth)
        image = spritesheet.subsurface(rect).copy()
        self.image = pygame.transform.smoothscale(image, (width, width))
        # Stores an alternate image, for purposes of the level editor
        impassible_overlay = pygame.image.load(constants.IMPASSIBLE_OVERLAY_PATH).convert_alpha()
        self.impassible_overlay = pygame.transform.smoothscale(impassible_overlay, (width, width))
        self.alt_img = pygame.transform.smoothscale(image, (width, width))
        self.alt_img.blit(self.impassible_overlay, (0, 0))

        self.sprite_flipped = False
        self.passable = True

    # Export tile as dictionary to be written to file
    def to_json(self):
        return {
            "world_loc": self.world_loc,
            "sprite_loc": self.sprite_loc,
            "flipped": self.sprite_flipped,
            "passable": self.passable
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
        # Alternate image has an overlay (denoting impassibility)
        self.alt_img = pygame.transform.smoothscale(image, (self.width, self.width))
        self.alt_img.blit(self.impassible_overlay, (0, 0))

    def swap_image(self):
        temp = self.alt_img
        self.alt_img = self.image
        self.image = temp