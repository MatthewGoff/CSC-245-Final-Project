# Health/energy bars
# Author: Caleb
# Winter 2017

import pygame

BAR_WIDTH = 10

class ResourceBar(pygame.sprite.Sprite):

    def __init__(self, x, y, width, max, color):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.image = pygame.Surface((self.width, BAR_WIDTH,))
        self.image.fill(pygame.color.Color(color))
        self.color = color
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, BAR_WIDTH)
        self.max = max
        self.curr = max

    def change(self, amount):
        if self.curr + amount > self.max:
            self.curr = self.max
        elif self.curr + amount < 0:
            self.curr = 0
        else:
            self.curr = self.curr + amount
        scalar = float(self.curr)/self.max
        self.image = pygame.Surface((int(self.width*scalar), BAR_WIDTH,))
        self.image.fill(pygame.color.Color(self.color))

    def set_pos(self, x, y):
        self.rect = pygame.Rect(x, y, self.width, BAR_WIDTH)

# Background for the health/energy bars
class BarBG(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.image = pygame.Surface((self.width, BAR_WIDTH*2,))
        self.image.fill(pygame.color.Color("darkgrey"))
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, BAR_WIDTH*2)

    def set_pos(self, x, y):
        self.rect = pygame.Rect(x, y, self.width, BAR_WIDTH * 2)