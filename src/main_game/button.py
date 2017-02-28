# A goddamn button class
# Author: Matthew Goff
# Winter 2017

import pygame

from util import draw_text


class Button:
    def __init__(self, rect, font_size, text, action):
        self.rect = rect
        self.font_size = font_size
        self.text = text
        self.action = action

    def click(self):
        self.action()

    def draw(self, window):
        pygame.draw.rect(window,
                         pygame.Color("DarkGrey"),
                         (self.rect.left,
                          self.rect.top, self.rect.width, self.rect.height),
                         3)

        draw_text(((self.rect.left + (self.rect.width / 2)),
                   (self.rect.top + (self.rect.height / 2))),
                  self.text,
                  self.font_size,
                  window)




