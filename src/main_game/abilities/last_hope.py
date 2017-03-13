# Will it be enough to save Union?
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
ENERGY_COST = 100
DAMAGE = 300
TICK_DAMAGE = 100
LAST_TICK = 10000


class LastHope(Ability):
    # Initialize sound
    pygame.mixer.init()
    sound = pygame.mixer.Sound("../assets/sounds/party_get.wav")

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.name = "Last Hope"
        self.width = WIDTH
        self.height = HEIGHT

        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        spritesheet = pygame.image.load("../assets/images/OtherSheet.png").convert_alpha()
        sprite_rect = pygame.Rect(1185, 192, 32, 32)
        image = spritesheet.subsurface(sprite_rect).copy()
        self.image = pygame.transform.smoothscale(image, (WIDTH, HEIGHT))

        icon_rect = pygame.Rect(640, 192, 32, 32)
        icon = spritesheet.subsurface(icon_rect).copy()
        self.icon = pygame.transform.smoothscale(icon, (ICON_WIDTH, ICON_HEIGHT))

        self.melee = False
        self.friends_usable = False
        self.enemies_usable = True
        self.has_effect = True

        self.effect = Tick()

        self.tooltip = Tooltip("Last Hope",
                               "100 Energy",
                               "The artifact is glowing softly")

    @classmethod
    def apply_effects(cls, enemy):
        enemy.hp.change(-DAMAGE)
        if enemy.hp.curr == 0:
            enemy.dead = True

        cls.sound.play(0,500)

    @classmethod
    def apply_cost(cls, user):
        user.energy.change(-ENERGY_COST)

    @classmethod
    def can_be_used_by(cls, user):
        return user.energy.curr >= ENERGY_COST


class Tick(Effect):

    def __init__(self):
        Effect.__init__(self)
        self.duration = 5

    def affect_targets(self, round):
        if round == self.end:
            self.target.hp.change(-LAST_TICK)
        else:
            self.target.hp.change(-TICK_DAMAGE)
        if self.target.hp.curr == 0:
            self.target.dead = True
