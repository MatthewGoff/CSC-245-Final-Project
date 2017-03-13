# Player class, player objects can be NPCs or user controlled
# Author: Caleb
# Vers: Winter 2017

import pygame, random
from resource_bar import ResourceBar, BarBG

BAR_WIDTH = 10


class Combatant(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, spritesheet_path, sprite_x, sprite_y, sprite_w, sprite_h, is_human):
        pygame.sprite.Sprite.__init__(self)
        self.is_human = is_human
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        sprite_rect = pygame.Rect(sprite_x, sprite_y, sprite_w, sprite_h)
        image = spritesheet.subsurface(sprite_rect).copy() # error
        self.image = pygame.transform.smoothscale(image, (width, height))
        self.speed = 1
        self.hp = ResourceBar(x, y - BAR_WIDTH*2, width, 100, "green")
        self.energy = ResourceBar(x, y - BAR_WIDTH, width, 100, "blue")
        self.bar_bg = BarBG(x, y - BAR_WIDTH*2, width)
        self.arm = 100
        self.str = 0
        self.dex = 0
        self.int = 0
        self.stam = 0
        self.dead = False
        self.abilities = []

        # Initialize sound
        pygame.mixer.init()
        self.atk_sound = pygame.mixer.Sound("../assets/sounds/player_attk.wav")

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.energy.set_pos(x, y - BAR_WIDTH)
        self.hp.set_pos(x, y - BAR_WIDTH*2)
        self.bar_bg.set_pos(x, y - BAR_WIDTH*2)

    def change_hp(self, amount):
        self.hp.change_max(amount)

    def attack(self, enemy):
        amount = random.randint(15, 25)

        self.energy.change(-10)
        enemy.hp.change(-amount)
        self.atk_sound.play(0, 250)
        if enemy.hp.curr == 0:
            enemy.dead = True

    def use_ability(self, ability, target, effects, round):
        ability.apply_cost(self)
        if ability.has_effect:
            ability.add_effect(effects, target, round)
        ability.apply_effects(target)

    def can_use(self, ability, target):
        return ability.can_be_used_by(self) and ability.can_be_used_on(target)








