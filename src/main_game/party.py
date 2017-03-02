# Party class stores data of NPC or user parties
# Author: Matthew Goff
# Winter 2017

import pygame

from util import Vec2D


class Party(pygame.sprite.Sprite):

    def __init__(self, position, radius, image, world):
        pygame.sprite.Sprite.__init__(self)

        self.position = Vec2D(position[0],position[1])
        self.velocity = Vec2D(0, 0)
        self.radius = radius
        self.world = world

        # 3. Define self.image
        self.image = image
        self.image = pygame.transform.smoothscale(self.image, (32, 45))

        # 4. Positions the Sprite
        self.update_rect()

    # Sets the forces from user input to the player.
    def set_velocity(self, x, y):
        self.velocity = Vec2D(x, y)

    # Updates rect instance variable for Sprite to the position the ball is at.
    def update_rect(self):
        self.rect = pygame.Rect(self.position.x-self.radius,
                                self.position.y-self.radius,
                                self.radius*2,
                                self.radius*2)

    def simulate(self, dt):
        next_position = self.position + self.velocity*dt
        parties = self.world.collide_parties(self)
        for party in parties:
            pass
            # Battle

        tiles = self.world.collide_tiles(self)
        move = True
        for tile in tiles:
            if tile.door:
                pass
            elif tile.impassible:
                move = False

        if move:
            self.position = next_position

        self.update_rect()

    def draw(self, window):
        window.blit(self.image,
                    (self.position.x-self.radius, self.position.y-self.radius))