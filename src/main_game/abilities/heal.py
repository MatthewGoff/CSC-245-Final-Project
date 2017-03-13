# Heals self or ally
# Author: Caleb
# Winter 2017

import pygame
from ability import Ability
from tooltip import Tooltip

ICON_WIDTH = 40
ICON_HEIGHT = 40
HEAL_AMOUNT = 200
ENERGY_COST = 40

class Heal(Ability):

    has_effect = False
    # Initialize sound
    pygame.mixer.init()
    sound = pygame.mixer.Sound("../assets/sounds/player_heal.wav")

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.name = "Heal"

        self.rect = None
        spritesheet = pygame.image.load("../assets/images/OtherSheet.png").convert_alpha()
        self.image = None

        icon_rect = pygame.Rect(1248, 320, 32, 32)
        icon = spritesheet.subsurface(icon_rect).copy()
        self.icon = pygame.transform.smoothscale(icon, (ICON_WIDTH, ICON_HEIGHT))

        self.energy_cost = ENERGY_COST

        self.melee = False
        self.friends_usable = True
        self.enemies_usable = False

        self.tooltip = Tooltip("Heal",
                               "40 Energy",
                               "Restores the health of an ally (or yourself!)")

    @classmethod
    def apply_effects(cls, friend):
        friend.hp.change(HEAL_AMOUNT)
        cls.sound.play(0,500)

    @classmethod
    def apply_cost(cls, user):
        user.energy.change(-ENERGY_COST)

    @classmethod
    def can_be_used_by(cls, user):
        return user.energy.curr >= ENERGY_COST

    @classmethod
    def can_be_used_on(cls, target):
        return target.hp.curr < target.hp.max