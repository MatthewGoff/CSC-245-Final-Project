# Some utilities
# Author: Matthew Goff
# Winter 2017

import pygame


def get_native_size():
    pygame.init()
    info = pygame.display.Info()
    return info.current_w, info.current_h
