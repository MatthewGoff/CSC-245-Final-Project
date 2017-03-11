# An ability to recharge energy. Castable on self or ally
# Author: Caleb
# Winter 2017

import pygame
from ability import Ability
from tooltip import Tooltip

ICON_WIDTH = 40
ICON_HEIGHT = 40
RECHARGE_AMOUNT = 60

class Energize(Ability):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.name = "Energize"

        self.rect = None
        spritesheet = pygame.image.load("../assets/images/OtherSheet.png").convert_alpha()
        self.image = None

        icon_rect = pygame.Rect(96, 256, 32, 32)
        icon = spritesheet.subsurface(icon_rect).copy()
        self.icon = pygame.transform.smoothscale(icon, (ICON_WIDTH, ICON_HEIGHT))

        self.energy_cost = 0

        self.melee = False
        self.friends_usable = True
        self.enemies_usable = False

        self.tooltip = Tooltip("Energize",
                               "No Cost",
                               "Recharge the energy of an ally (or yourself!)")

    @classmethod
    def apply_effects(cls, friend):
        friend.energy.change(RECHARGE_AMOUNT)

    @classmethod
    def can_be_used_on(cls, target):
        return target.energy.curr < target.energy.max