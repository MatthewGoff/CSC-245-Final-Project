# Party class stores data of NPC or user parties
# Author: Matthew Goff
# Winter 2017

import pygame

from util import Vec2D
from door import Door


class Party(pygame.sprite.Sprite):

    # Initialize sound
    pygame.mixer.init()

    # The width and height of the player sprite sheet.
    _width = 576
    _height = 48
    # The numbers of player sprites on the sprite sheet
    _number = 12
    # The height and width of one player sprite is 48 pixels.
    _length = 48

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

        # Keeps all the moving sprites
        self.mov_imgs = []
        # Keeps all the standing/stop sprites
        self.stp_imgs = []

        self.rect = pygame.Rect(self.position.x - hitbox[0] / 2,
                                  self.position.y - hitbox[1] / 2,
                                  hitbox[0],
                                  hitbox[1])
        # 4. Positions the Sprite
        self.hitbox = pygame.Rect(self.position.x - hitbox[0] / 2,
                                  self.position.y - hitbox[1] / 2,
                                  hitbox[0],
                                  hitbox[1])

        self.battle_listener = battle_listener
        self.friendly = False

        self.members = []

        self.controllable = False
        self.direction = 0

        pygame.mixer.init()
        self.walk_sound = pygame.mixer.Sound("../assets/sounds/player_walk.wav")
        self.party_get_sound = pygame.mixer.Sound("../assets/sounds/party_get.wav")

    def change_size(self, factor):
        self.rect = pygame.Rect(self.position.x - (self.rect.w*factor)/2,
                                self.position.y - (self.rect.h*factor)/2,
                                self.rect.w*factor,
                                self.rect.h*factor)
        self.hitbox = pygame.Rect(self.position.x - (self.hitbox.w*factor)/2,
                                self.position.y - (self.hitbox.h*factor)/2,
                                self.hitbox.w*factor,
                                self.hitbox.h*factor)
        self.sprite_width *= factor

    def set_velocity(self, x, y):
        self.velocity = Vec2D(x, y)

    def set_pos(self, pos):
        self.position = Vec2D(pos[0], pos[1])

    def change_img(self, path):
        self.full_img = pygame.image.load(path).convert_alpha()

    def update_rect(self):
        self.rect.center = self.position.to_tuple()
        self.hitbox.center = self.position.to_tuple()
        self.hitbox.center = (self.hitbox.center[0], self.hitbox.center[1] + 10)

    def make_controllable(self, image):
        # Loads the full player image as a surface, sets the
        # index to default zero
        self.full_img = pygame.image.load(image).convert_alpha()
        self.index = 0

        # Adds each part of player action pic as a subsurface
        if len(self.mov_imgs) == 0:
            self.mov_imgs = [self.full_img.subsurface(pygame.Rect((i * self._length, 0), (self._length, self._length)))
                             for i in xrange(self._number)]

        # Separates sprites into two list: one keeps all moving
        # sprites, one keeps all standing/stop sprites.
        self.stp_imgs = [self.mov_imgs[1], self.mov_imgs[10], self.mov_imgs[4], self.mov_imgs[7]]

        # Why len - 2 here? Because when the player is moving
        # to the left or right, three sprites (left step, stand,
        # right step)
        for i in range(0, len(self.stp_imgs) - 2):
            self.mov_imgs.remove(self.stp_imgs[i])

        # Standard requirements of Sprite obj for drawing
        self.image = self.stp_imgs[self.index]
        self.rect = pygame.Rect(self.position.x, self.position.y, self._width, self._height)

        self.controllable = True

    def make_friendly(self):
        self.friendly = True

    def change_hitbox(self, rect):
        self.hitbox = rect

    def merge_with(self, party2):
        for player in party2.members:
            self.members += [player]
        party2.world.remove_party(party2)
        self.party_get_sound.play(0, 500)

    def simulate(self, dt, time):
        door = None
        self.position += self.velocity*dt
        self.update_rect()
        if self.controllable:
            self.apply_animation(time)

        parties = self.world.collide_parties(self)
        for party in parties:
            if not party.friendly:
                self.battle_listener(party)
            elif not party.controllable:
                self.merge_with(party)
                door = "meet_prompt"
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

    def apply_animation(self, time):
        if self.velocity.x > 0:
            self.right_moving(time)
            self.direction = 1
        elif self.velocity.x < 0:
            self.left_moving(time)
            self.direction = 2
        elif self.velocity.y > 0:
            self.face_moving(time)
            self.direction = 3
        elif self.velocity.y < 0:
            self.back_moving(time)
            self.direction = 4
        else:
            if self.direction == 1:
                self.right_stop()
            elif self.direction == 2:
                self.left_stop()
            elif self.direction == 3:
                self.face_stop()
            elif self.direction == 4:
                self.back_stop()
            self.direction = 0

    def stop(self):
        self.velocity = Vec2D(0,0)

    # When pressing s, player moves down to the screen by steps
    def face_moving(self, time):
        if time % 12 < 2:
            self.walk_sound.play(0, 500)
            self.index += 1
        if not 0 <= self.index <= 1:
            self.index = 0
        self.image = self.mov_imgs[self.index]

    # When pressing w, player moves up to the screen by steps
    def back_moving(self, time):
        if time % 12 < 2:
            self.walk_sound.play(0, 500)
            self.index += 1
        if not 8 <= self.index <= 9:
            self.index = 8
        self.image = self.mov_imgs[self.index]

    # When pressing a, player moves left to the screen by steps
    def left_moving(self, time):
        if time % 12 < 2:
            self.walk_sound.play(0, 500)
        if time % 6 < 3:
            self.index += 1
        if not 2 <= self.index <= 4:
            self.index = 2
        self.image = self.mov_imgs[self.index]

    # When pressing d, player moves right to the screen by steps
    def right_moving(self, time):
        if time % 12 < 2:
            self.walk_sound.play(0, 500)
        if time%6 < 3:
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