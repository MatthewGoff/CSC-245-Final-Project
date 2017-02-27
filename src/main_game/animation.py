# Animations for player
# @author Yunmeng Li
# @version Winter, 2017

import pygame

class PlayerAnimation(pygame.sprite.Sprite):

    _width = 576
    _height = 48
    _number = 12
    images = []

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y

        # loading the full player image as a surface, set the index to default zero
        self.full_img = pygame.image.load("player.png").convert_alpha()
        self.index = 0

        if len(self.images) == 0:
            # add each part of player action pic as a subsurface
            # there are 12 separate parts
            self.images = [self.full_img.subsurface(pygame.Rect( (i * 48,0),(48,48)))
                         for i in xrange(self._number)]

        # make a list of subsurface
        self.image = self.images[self.index+1]
        self.rect = pygame.Rect(x, y, self._width, self._height)

    def face_moving(self):
        # index 0 to 2 are for face movement
        self.index = 0
        self.image = self.images[self.index]

        "Tried to switch pictures here, but failed."
        #pygame.time.wait(100)
        #self.index = 2
        #self.image = self.images[self.index]

    def left_moving(self):
        # index 3 and 5 are for left movement
        self.index = 3
        self.image = self.images[self.index]

    def right_moving(self):
        # index 6 and 8 are for right movement
        self.index = 6
        self.image = self.images[self.index]

    def back_moving(self):
        # index 9 and 11 are for back movement
        self.index = 9
        self.image = self.images[self.index]

    def face_stop(self):
        self.image = self.images[1]

    def left_stop(self):
        self.image = self.images[4]

    def right_stop(self):
        self.image = self.images[7]

    def back_stop(self):
        self.image = self.images[10]
