# A more powerful melee attack
# Author: Caleb
# Winter 2017

import pygame
from ability import Ability
from tooltip import Tooltip

ICON_WIDTH = 40
ICON_HEIGHT = 40
DAMAGE = 60
HP_COST = 25

class PowerAttack(Ability):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.name = "Power Attack"

        self.rect = None
        spritesheet = pygame.image.load("../assets/images/OtherSheet.png").convert_alpha()
        self.image = None

        icon_rect = pygame.Rect(64, 1504, 32, 32)
        icon = spritesheet.subsurface(icon_rect).copy()
        self.icon = pygame.transform.smoothscale(icon, (ICON_WIDTH, ICON_HEIGHT))

        self.melee = True
        self.friends_usable = False
        self.enemies_usable = True
        self.has_effect = False

        self.tooltip = Tooltip("Power Attack",
                               "25 Health",
                               "An all-out melee attack, the execution of which "
                               "will be painful for both you and the enemy")

    @classmethod
    def apply_effects(cls, enemy):
        enemy.hp.change(-DAMAGE)
        if enemy.hp.curr == 0:
            enemy.dead = True

    @classmethod
    def apply_cost(cls, user):
        user.hp.change(-HP_COST)

    @classmethod
    def can_be_used_by(cls, user):
        return user.hp.curr >= HP_COST