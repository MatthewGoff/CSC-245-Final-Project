#
# Author: Caleb
# Winter 17

import pygame


class SpriteViewer:
    color = pygame.color.Color("Red")
    curr_row = 0
    padding = 8
    selected_index = 0
    SPRITE_WIDTH = 32

    def __init__(self, x, y, width, height, spritesheet, tile_width):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tile_width = tile_width
        self.sprites_per_row = (width - self.padding) / (tile_width + self.padding)
        self.num_rows = (height - self.padding) / (tile_width + self.padding)
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.select_indicator = pygame.Surface((tile_width + 8, tile_width + 8))
        self.select_indicator.fill(self.color)
        self.sprites = []
        self.rects = []
        for i in range(spritesheet.get_height()/SpriteViewer.SPRITE_WIDTH):
            for j in range(spritesheet.get_width()/SpriteViewer.SPRITE_WIDTH):
                rect = pygame.Rect(j*SpriteViewer.SPRITE_WIDTH,
                                   i*SpriteViewer.SPRITE_WIDTH,
                                   SpriteViewer.SPRITE_WIDTH,
                                   SpriteViewer.SPRITE_WIDTH)
                image = spritesheet.subsurface(rect).copy()
                self.sprites += [pygame.transform.smoothscale(image, (tile_width, tile_width))]
                self.rects += [rect]



    def draw(self, window):

        y = self.padding
        for i in range(self.num_rows):
            if i < len(self.sprites)/self.sprites_per_row:
                self.draw_row(self.curr_row + i, y, window)
            y += self.tile_width + self.padding

    def draw_row(self, row, y, window):
        x = self.padding
        for i in range(self.sprites_per_row):
            if row * self.sprites_per_row + i == self.selected_index:
                window.blit(self.select_indicator, (x-4, y-4))
            if row * self.sprites_per_row + i < len(self.sprites):
                window.blit(self.sprites[row * self.sprites_per_row + i], (x, y))
            x += self.tile_width + self.padding

    def click_sprite(self, pos):
        x,y = pos[0],pos[1]
        if x > self.padding and y > self.padding:
            column = (x - self.padding) / (self.tile_width + self.padding)
            row = (y - self.padding) / (self.tile_width + self.padding)
            self.select_sprite(column, row)

    def select_sprite(self, column, row):
        true_row = self.curr_row + row
        selected_index = true_row * self.sprites_per_row + column
        if selected_index < len(self.sprites):
            self.selected_index = selected_index

    def get_rect(self):
        return self.rects[self.selected_index]