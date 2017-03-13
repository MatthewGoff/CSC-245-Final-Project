# Party class stores data of NPC or user parties
# Author: Matthew Goff
# Winter 2017

import pygame

from util import Vec2D
from door import Door


class Party(pygame.sprite.Sprite):

    # The width and height of the player sprite sheet.
    _width = 576
    _height = 48
    # The numbers of player sprites on the sprite sheet
    _number = 12
    # The height and width of one player sprite is 48 pixels.
    _length = 48
    # Keeps all the moving sprites
    mov_imgs = []
    # Keeps all the standing/stop sprites
    stp_imgs = []

    def __init__(self, position, sprite_width, hitbox, image, world, battle_listener):
    #def __init__(self, position, sprite_width, hitbox, world, battle_listener):
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
        'Old'
        #self.image = image
        #self.image = pygame.transform.smoothscale(self.image, (sprite_width, sprite_width))

        'New'
        # Loads the full player image as a surface, sets the
        # index to default zero
        self.full_img = pygame.image.load("../assets/images/player.png").convert_alpha()
        self.index = 0

        # Adds each part of player action pic as a subsurface
        if len(self.mov_imgs) == 0:
            self.mov_imgs = [self.full_img.subsurface(pygame.Rect((i * self._length,0),(self._length,self._length)))
                         for i in xrange(self._number)]

        # Separates sprites into two list: one keeps all moving
        # sprites, one keeps all standing/stop sprites.
        self.stp_imgs = [self.mov_imgs[1], self.mov_imgs[10], self.mov_imgs[4], self.mov_imgs[7]]

        # Why len - 2 here? Because when the player is moving
        # to the left or right, three sprites (left step, stand,
        # right step)
        for i in range(0, len(self.stp_imgs)-2):
            self.mov_imgs.remove(self.stp_imgs[i])

        # Standard requirements of Sprite obj for drawing
        self.image = self.stp_imgs[self.index]
        self.rect = pygame.Rect(self.position.x, self.position.y, self._width, self._height)

        # 4. Positions the Sprite
        self.hitbox = pygame.Rect(self.position.x - hitbox[0] / 2,
                                  self.position.y - hitbox[1] / 2,
                                  hitbox[0],
                                  hitbox[1])

        self.battle_listener = battle_listener
        self.friendly = False

        self.members = []

    def set_velocity(self, x, y):
        self.velocity = Vec2D(x, y)

    def set_pos(self, pos):
        self.position = Vec2D(pos[0], pos[1])

    def update_rect(self):
        self.rect.center = self.position.to_tuple()
        self.hitbox.center = self.position.to_tuple()
        self.hitbox.center = (self.hitbox.center[0], self.hitbox.center[1] + 10)

    def make_friendly(self):
        self.friendly = True

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
            if not party.friendly:
                self.battle_listener(party)
            else:
                self.merge_with(party)
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

    # Makes the player walk by updating its position
    def walk(self, dx, dy):
        self.velocity = Vec2D(dx, dy)
        self.position += self.velocity

    # When pressing s, player moves down to the screen by steps
    def face_moving(self):
        self.index += 1
        if not 0 <= self.index <= 1:
            self.index = 0
        self.image = self.mov_imgs[self.index]

    # When pressing w, player moves up to the screen by steps
    def back_moving(self):
        self.index += 1
        if not 8 <= self.index <= 9:
            self.index = 8
        self.image = self.mov_imgs[self.index]

    # When pressing a, player moves left to the screen by steps
    def left_moving(self):
        self.index += 1
        if not 2 <= self.index <= 4:
            self.index = 2
        self.image = self.mov_imgs[self.index]

    # When pressing d, player moves right to the screen by steps
    def right_moving(self):
        self.index += 1
        if not 5 <= self.index <= 7:
            self.index = 5
        self.image = self.mov_imgs[self.index]

    # Sets the player to stop, facing to the screen
    def face_stop(self):
        self.image = self.stp_imgs[0]

    # Sets the player to stop, turning back to the screen
    def back_stop(self):
        self.image = self.stp_imgs[1]

    # Sets the player to stop, facing to the left
    def left_stop(self):
        self.image = self.stp_imgs[2]

    # Sets the player to stop, facing to the right
    def right_stop(self):
        self.image = self.stp_imgs[3]