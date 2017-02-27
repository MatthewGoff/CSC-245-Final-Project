# A class for world
# Author: Caleb
# Winter 2017

import json

import pygame
from main_game.tile import Tile


class World:
    TILE_WIDTH = 40
    SPRITE_WIDTH = 32

    def __init__(self, x, y, spritesheet):

        self.width = x
        self.height = y
        self.tile_width = World.TILE_WIDTH
        self.sprite_width = World.SPRITE_WIDTH
        self.bg_sprites = pygame.sprite.Group()
        self.fg_sprites = pygame.sprite.Group()
        self.spritesheet = spritesheet

        self.foreground_tiles = []
        self.background_tiles = []
        for row in range(y):
            self.foreground_tiles += [[]]
            self.background_tiles += [[]]

            for column in range(x):
                newTile = Tile(column*self.tile_width,
                               row*self.tile_width,
                               self.tile_width,
                               self.spritesheet,
                               (1856, 448),
                               World.SPRITE_WIDTH)
                self.bg_sprites.add(newTile)
                self.foreground_tiles[row] += [None]
                self.background_tiles[row] += [newTile]
        self.border = pygame.Rect(0, 0, x * self.tile_width, y * self.tile_width)

    @classmethod
    def load(cls, name):
        world = World(0, 0, pygame.image.load(
            "../assets/images/OtherSheet.png").convert_alpha())
        world.import_world("../assets/worlds/"+name+".json")
        return world

    def draw(self, window):
        self.bg_sprites.draw(window)
        self.fg_sprites.draw(window)

    # Returns a the result of drawing the world, but only actually draws the part that will appear in the
    # clip_rect.  This saves a lot of resources because the world may be much larger than the part that will
    # appear on the screen.
    def get_draw_buffer(self, clip_rect):

        # Makes an empty buffer of the size of the world.  The buffer is transparent, so they can be overlayed.
        buffer = pygame.Surface((self.border.w, self.border.h), pygame.SRCALPHA, 32)
        # Indicates the clipping rectangle.  Subsequent draws to this buffer will only draw if the result would
        # appear in the clipping rectangle.
        buffer.set_clip(clip_rect)
        buffer = buffer.convert_alpha()
        self.draw(buffer)

        return buffer

    def get_border(self):
        return self.border

    def get_bg_tile(self, x, y):
        return self.background_tiles[y][x]

    def get_fg_tile(self, x, y):
        return self.foreground_tiles[y][x]

    def add_foreground_tile(self, x, y, sprite_rect):
        tile = Tile(x*self.tile_width, y*self.tile_width, self.tile_width, self.spritesheet, (33, 33), self.sprite_width)
        tile.change_sprite(sprite_rect)
        self.fg_sprites.add(tile)
        self.foreground_tiles[y][x] = tile

    def export_world(self, path):
        background_tiles = []
        for row in self.background_tiles:
            json_tiles = []
            for tile in row:
                json_tiles += [tile.to_json()]
            background_tiles += [json_tiles]

        foreground_tiles = []
        for row in self.foreground_tiles:
            json_tiles = []
            for tile in row:
                if tile:
                    json_tiles += [tile.to_json()]
                else:
                    json_tiles += [None]
            foreground_tiles += [json_tiles]

        write_object = {
            "background": background_tiles,
            "foreground": foreground_tiles
        }

        with open(path, 'w') as outfile:
            json.dump(write_object, outfile)

    def import_world(self, path):
        data = json.load(open(path))

        self.background_tiles = []
        self.bg_sprites = pygame.sprite.Group()
        for row in range(self.height):
            self.background_tiles += [[]]

            for column in range(self.width):
                tile_json = data["background"][row][column]
                new_tile = Tile(tile_json["x"],
                                tile_json["y"],
                                tile_json["width"],
                                self.spritesheet,
                                tile_json["spriteLoc"],
                                tile_json["spriteWidth"])
                self.bg_sprites.add(new_tile)
                self.background_tiles[row] += [new_tile]

        self.foreground_tiles = []
        self.fg_sprites = pygame.sprite.Group()
        for row in range(self.height):
            self.foreground_tiles += [[]]

            for column in range(self.width):
                tile_json = data["foreground"][row][column]
                if tile_json:
                    new_tile = Tile(tile_json["x"],
                                    tile_json["y"],
                                    tile_json["width"],
                                    self.spritesheet,
                                    tile_json["spriteLoc"],
                                    tile_json["spriteWidth"])
                    self.fg_sprites.add(new_tile)
                    self.foreground_tiles[row] += [new_tile]
                else:
                    new_tile = None
                    self.foreground_tiles[row] += [new_tile]
