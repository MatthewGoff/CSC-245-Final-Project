# A class for world
# Author: Caleb
# Winter 2017

import json

import pygame

from tile import Tile

class World:
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    spritesheet = pygame.image.load("../images/HolySheet.png").convert_alpha()
    rows = []

    def __init__(self, x, y, tile_width, center, spritesheet, sprite_width):

        self.sprite_width = sprite_width
        self.width = x
        self.height = y
        self.tile_sprites = pygame.sprite.Group()
        self.spritesheet = spritesheet

        for row in range(y):
            self.rows += [[]]

            for column in range(x):
                newTile = Tile(column*tile_width, row*tile_width, tile_width, self.spritesheet, (1856, 448), self.sprite_width)
                self.tile_sprites.add(newTile)

                self.rows[row] += [newTile]
        self.border = pygame.Rect(0, 0, x * tile_width, y * tile_width)
        self.center = center

    def draw(self, window):
        self.tile_sprites.draw(window)


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

    def get_tile(self, x, y):
        return self.rows[y][x]

    def export_world(self):
        name = raw_input("Please enter the desired filename: ")

        write_object = []
        for row in self.rows:
            rowStr = []
            for tile in row:
                rowStr += [tile.to_json()]
            write_object += [rowStr]

        with open("../worlds/"+name+'.json', 'w') as outfile:
            json.dump(write_object, outfile)
            print "saved world!"

    def import_world(self):
        name = raw_input("Please enter the desired filename: ")

        try:
            data = json.load(open("../worlds/"+name+".json"))
        except IOError:
            print("Couldn't find that file")
            return

        self.rows = []
        self.tile_sprites = pygame.sprite.Group()
        for row in range(self.height):
            self.rows += [[]]

            for column in range(self.width):
                new_tile = Tile(data[row][column]["x"],
                                data[row][column]["y"],
                                data[row][column]["width"],
                                self.spritesheet,
                                data[row][column]["spriteLoc"],
                                data[row][column]["spriteWidth"])
                self.tile_sprites.add(new_tile)
                self.rows[row] += [new_tile]
