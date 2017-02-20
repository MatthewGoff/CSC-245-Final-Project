
from tile import Tile
import pygame

class World:
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    spritesheet = pygame.image.load("images/HolySheet.png").convert_alpha()
    rows = []

    def __init__(self, x, y, tile_width, center, spritesheet, sprite_width):

        self.sprite_width = sprite_width
        self.width = x*self.sprite_width
        self.height = y*self.sprite_width
        self.tile_sprites = pygame.sprite.Group()
        self.spritesheet = spritesheet

        for row in range(y):
            self.rows += [[]]

            for column in range(x):
                newTile = Tile(column*tile_width, row*tile_width, tile_width, self.spritesheet, (512, 128), self.sprite_width)
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
        file = open(name + ".txt", "w")
        for row in self.rows:
            rowStr = ""
            for tile in row:
                rowStr += str(tile)
            file.write(rowStr + "\n")
        file.close()

