
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, spritesheet, spriteLoc, spriteWidth):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, width)

        self.x = x
        self.y = y
        self.width = width
        self.spritesheet = spritesheet
        self.spriteLoc = spriteLoc
        self.spriteWidth = spriteWidth
        rect = pygame.Rect(spriteLoc[0], spriteLoc[1], self.spriteWidth, self.spriteWidth)
        image = spritesheet.subsurface(rect).copy()
        self.image = pygame.transform.smoothscale(image, (width, width))


    def __str__(self):
        output = ""
        output += str(self.x) + "/"
        output += str(self.y) + "/"
        output += str(self.width)  + "/"
        output += str(self.spriteLoc[0]) + "/"
        output += str(self.spriteLoc[1]) + "/"
        output += str(self.spriteWidth) + " "

        return output



    def readable_string(self):
        return "sprite at position " + str(self.spriteLoc) + " at (" + str(self.x) + ", " + str(self.y) + ")"

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def change_sprite(self, sprite):
        self.image = pygame.transform.smoothscale(sprite, (self.width, self.width))

    def change_sprite2(self, spriteLoc):
        self.spriteLoc = spriteLoc
        rect = pygame.Rect(spriteLoc[0], spriteLoc[1], self.spriteWidth, self.spriteWidth)
        image = self.spritesheet.subsurface(rect).copy()
        self.image = pygame.transform.smoothscale(image, (self.width, self.width))