# Party class stores data of NPC or user parties
# Author: Matthew Goff
# Winter 2017

import pygame

from util import Vec2D
from door import Door


class Party(pygame.sprite.Sprite):

    def __init__(self, position, sprite_width, hitbox, image, world, battle_listener):
        """

        :param position:
        :param sprite_width:
        :param hitbox: A 2-tuple (width, height) of the hitbox centered at param position
        :param image:
        :param world:
        """
        pygame.sprite.Sprite.__init__(self)

        self.position = Vec2D(position[0],position[1])
        self.velocity = Vec2D(0, 0)
        self.sprite_width = sprite_width
        self.world = world

        # 3. Define self.image
        self.image = image
        self.image = pygame.transform.smoothscale(self.image, (sprite_width, sprite_width))

        # 4. Positions the Sprite
        self.rect = pygame.Rect(self.position.x - self.sprite_width / 2,
                                self.position.y - self.sprite_width / 2,
                                self.sprite_width,
                                self.sprite_width)
        self.hitbox = pygame.Rect(self.position.x - hitbox[0] / 2,
                                  self.position.y - hitbox[1] / 2,
                                  hitbox[0],
                                  hitbox[1])

        self.battle_listener = battle_listener

        self.members = []

    def set_velocity(self, x, y):
        self.velocity = Vec2D(x, y)

    def set_pos(self, pos):
        self.position = Vec2D(pos[0], pos[1])

    def update_rect(self):
        self.rect.center = self.position.to_tuple()
        self.hitbox.center = self.position.to_tuple()

    def change_hitbox(self, rect):
        self.hitbox = rect

    def merge_with(self, party2):
        for player in party2.members:
            self.members += [player]
        party2.world.remove_party(party2)

    def simulate(self, dt):
        door = None
        self.position += self.velocity*dt
        self.update_rect()

        parties = self.world.collide_parties(self)
        for party in parties:
            self.battle_listener(party)
        tiles = self.world.collide_tiles(self)
        collision = False
        for tile in tiles:
            if isinstance(tile, Door):
                door = tile
            if not tile.passable:
                collision = True
        if collision:
            self.position -= self.velocity * dt
            self.update_rect()

        return door

    def draw(self, window):
        window.blit(self.image,
                    (self.position.x - self.sprite_width / 2, self.position.y - self.sprite_width / 2))