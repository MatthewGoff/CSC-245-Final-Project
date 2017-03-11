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


def draw_text(center, text, font_size, window):
    font = pygame.font.SysFont("freesansbold.ttf", font_size)
    text_surface = font.render(text, True, pygame.Color("black"))
    text_rect = text_surface.get_rect()
    text_rect.center = center
    window.blit(text_surface, text_rect)

# A text input box in pygame that writes to a given dictionary
# Note that x and y are relative to the surface on which it's drawn
class TextInputBox:
    def __init__(self, x, y, width, key, output_dict):
        pygame.init()
        self.font = pygame.font.SysFont("monospace", 14)
        self.x = x
        self.y = y
        self.width = width
        self.rect = pygame.Rect(x, y, width, 16)
        self.surface = pygame.Surface((width, 16))
        self.surface.fill(pygame.color.Color("darkgrey"))
        self.text = None
        self.active = False
        output_dict[key] = ""
        self.key = key
        self.output_dict = output_dict

    def select(self):
        self.active = True
        self.surface.fill(pygame.color.Color("lightgrey"))
        if self.text is not None:
            self.surface.blit(self.text, (0,0))

    def deselect(self):
        self.active = False
        self.surface.fill(pygame.color.Color("darkgrey"))
        if self.text is not None:
            self.surface.blit(self.text, (0,0))

    # key_pressed is the mod 256 number for the pressed key
    def handle_keydown(self, key_pressed):
        update_img = False
        print key_pressed
        # Letters, numbers and space
        if 48 <= key_pressed <= 57 or 97 <= key_pressed <= 122 or key_pressed == pygame.K_SPACE:
            self.output_dict[self.key] += str(chr(key_pressed))
            update_img = True
        elif key_pressed == pygame.K_MINUS and pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.output_dict[self.key] += "_"
            update_img = True
        elif key_pressed == pygame.K_BACKSPACE and not self.output_dict[self.key] == "":
            self.output_dict[self.key] = self.output_dict[self.key][0:-1]
            update_img = True
        #
        if update_img:
            self.surface = pygame.Surface((self.width, 16))
            self.surface.fill(pygame.color.Color("lightgrey"))
            self.text = self.font.render(self.output_dict[self.key], True, pygame.color.Color("Black"))
            self.surface.blit(self.text, (0,0))

    def draw(self, window):
        window.blit(self.surface, (self.x, self.y))











