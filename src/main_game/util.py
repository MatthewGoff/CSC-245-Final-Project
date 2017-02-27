# Some utilities
# Author: Matthew Goff
# Winter 2017

import pygame


def get_native_size():
    pygame.init()
    info = pygame.display.Info()
    return info.current_w, info.current_h


class Vec2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vec2D(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return Vec2D(self.x / scalar, self.y / scalar)

    def dot(self, other):
        return self.x*other.x+self.y*other.y

    def mag(self):
        return (self.get_x()**2+self.get_y()**2)**.5

    def is_zero(self):
        return self.x == 0 and self.y == 0

    def unit(self):
        if self.is_zero():
            return Vec2D(0, 0)
        else:
            return self/self.mag()

    def perp(self):
        return Vec2D(-1 * self.y, self.x)

    def to_tuple(self):
        return self.x, self.y

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x

    def __str__(self):
        return "<"+str(self.get_x())+","+str(self.get_y())+">"