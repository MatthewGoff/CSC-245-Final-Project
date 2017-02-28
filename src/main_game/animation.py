# Animations for player
# @author Yunmeng Li
# @version Winter, 2017

import pygame


class PlayerAnimation(pygame.sprite.Sprite):

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

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)

        # The position of the player, left-up corner
        self.x = x
        self.y = y
        self.speed = 10

        # Loads the full player image as a surface, sets the
        # index to default zero
        self.full_img = pygame.image.load("player.png").convert_alpha()
        self.index = 0

        # Adds each part of player action pic as a subsurface
        if len(self.mov_imgs) == 0:
            self.mov_imgs = [self.full_img.subsurface(pygame.Rect((i * self._length,0),(self._length,self._length)))
                         for i in xrange(self._number)]

        # Separates sprites into two list: one keeps all moving
        # sprites, one keeps all standing/stop sprites.
        self.stp_imgs = [self.mov_imgs[1], self.mov_imgs[4], self.mov_imgs[7], self.mov_imgs[10]]
        for i in range(0, len(self.stp_imgs)):
            self.mov_imgs.remove(self.stp_imgs[i])

        # Standard requirements of Sprite obj for drawing
        self.image = self.stp_imgs[self.index]
        self.rect = pygame.Rect(x, y, self._width, self._height)

    # Getter for x
    def get_x(self):
        return self.rect.x

    # Getter for y
    def get_y(self):
        return self.rect.y

    # Setter for x
    def set_x(self, x):
        self.rect.x = x

    # Setter for x
    def set_y(self, y):
        self.rect.y = y

    # Makes the player walk by updating its position
    def walk(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    # When pressing s, player moves down to the screen by steps
    def face_moving(self):
        self.index += 1
        if self.index > 1:
            self.index = 0
        self.image = self.mov_imgs[self.index]

    # When pressing w, player moves up to the screen by steps
    def back_moving(self):
        self.index += 1
        if self.index > 7 or self.index < 6:
            self.index = 6
        self.image = self.mov_imgs[self.index]

    # When pressing a, player moves left to the screen by steps
    def left_moving(self):
        self.index += 1
        if self.index > 3 or self.index < 2:
            self.index = 2
        self.image = self.mov_imgs[self.index]

    # When pressing d, player moves right to the screen by steps
    def right_moving(self):
        self.index += 1
        if self.index > 5 or self.index < 4:
            self.index = 4
        self.image = self.mov_imgs[self.index]

    # Sets the player to stop, facing to the screen
    def face_stop(self):
        self.image = self.stp_imgs[0]

    # Sets the player to stop, turning back to the screen
    def back_stop(self):
        self.image = self.stp_imgs[3]

    # Sets the player to stop, facing to the left
    def left_stop(self):
        self.image = self.stp_imgs[1]

    # Sets the player to stop, facing to the right
    def right_stop(self):
        self.image = self.stp_imgs[2]
