# Fireball ability
# Author: Caleb
# "Winter" 2017

import pygame
from ability import Ability
from tooltip import Tooltip
from effect import Effect

WIDTH = 20
HEIGHT = 20
ICON_WIDTH = 40
ICON_HEIGHT = 40
ENERGY_COST = 30
DAMAGE = 40
BURN_DAMAGE = 10


class Fireball(Ability):

    def __init__(self, x, y, int):
        pygame.sprite.Sprite.__init__(self)
        self.name = "Fireball"
        self.x = x
        self.y = y
        self.width = WIDTH
        self.height = HEIGHT

        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)
        spritesheet = pygame.image.load("../assets/images/OtherSheet.png").convert_alpha()
        sprite_rect = pygame.Rect(1185, 192, 32, 32)
        image = spritesheet.subsurface(sprite_rect).copy()
        self.image = pygame.transform.smoothscale(image, (WIDTH, HEIGHT))

        icon_rect = pygame.Rect(288, 1376, 32, 32)
        icon = spritesheet.subsurface(icon_rect).copy()
        self.icon = pygame.transform.smoothscale(icon, (ICON_WIDTH, ICON_HEIGHT))

        self.melee = False
        self.friends_usable = False
        self.enemies_usable = True
        self.has_effect = True

        self.effect = Burning()

        self.tooltip = Tooltip("Fireball",
                               "30 Energy",
                               "Hurls a fiery ball at the enemy, causing it to burn over time")

    @classmethod
    def apply_effects(cls, enemy):
        enemy.hp.change(-DAMAGE)
        if enemy.hp.curr == 0:
            enemy.dead = True

    @classmethod
    def apply_cost(cls, user):
        user.energy.change(-ENERGY_COST)

    @classmethod
    def can_be_used_by(cls, user):
        return user.energy.curr >= ENERGY_COST

class Burning(Effect):

    def __init__(self):
        Effect.__init__(self)
        self.duration = 2

    def affect_targets(self, round):
        print str(self.target) + " hp -10"
        print "round: " + str(round)
        print str(self.end)
        self.target.hp.change(-BURN_DAMAGE)
