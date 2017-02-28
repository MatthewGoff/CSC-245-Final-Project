#
# Author: Caleb
# Winter 17

import pygame

from main_game.constants import TILE_WIDTH


class SpriteViewer:
    PADDING = 8

    def __init__(self, x, y, width, height, spritesheet):

        self.color = pygame.color.Color("Red")
        self.curr_row = 0
        self.padding = SpriteViewer.PADDING
        self.selected_index = 0
        self.spritesheet = spritesheet

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tile_width = TILE_WIDTH

        self.sprites_per_row = (width - self.padding) / (self.tile_width + self.padding)
        self.num_rows = (height - self.padding) / (self.tile_width + self.padding)
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.select_indicator = pygame.Surface((self.tile_width + 8, self.tile_width + 8))
        self.select_indicator.fill(self.color)
        self.sprites = []
        self.rects = []
        for i in range(spritesheet.get_height()/self.tile_width):
            for j in range(spritesheet.get_width()/self.tile_width):
                rect = pygame.Rect(j*self.tile_width,
                                   i*self.tile_width,
                                   self.tile_width,
                                   self.tile_width)
                image = spritesheet.subsurface(rect).copy()
                self.sprites += [pygame.transform.smoothscale(image, (self.tile_width, self.tile_width))]
                self.rects += [rect]

        self.curr_display = pygame.Surface((width / 4, width / 4))
        self.curr_display.fill(pygame.color.Color("darkgrey"))
        self.display_current()
        self.sprite_flipped = False


    def display_current(self):
        selected_rect = self.rects[self.selected_index]
        image = self.spritesheet.subsurface(selected_rect).copy()
        self.selected_sprite = pygame.transform.smoothscale(image, ((self.width / 4), (self.width / 4)))


    def draw(self, window):

        y = self.padding
        for i in range(self.num_rows):
            if i < len(self.sprites)/self.sprites_per_row:
                self.draw_row(self.curr_row + i, y, window)
            y += self.tile_width + self.padding
        curr_display_pos = (int(self.width *.75), self.height - self.width/4)
        window.blit(self.curr_display, curr_display_pos)
        window.blit(self.selected_sprite, curr_display_pos)

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
            self.display_current()
            self.sprite_flipped = False

    def get_rect(self):
        return self.rects[self.selected_index]