
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

    def to_json(self):
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "spriteLoc": self.spriteLoc,
            "spriteWidth": self.spriteWidth
        }

    def readable_string(self):
        return "sprite at position " + str(self.spriteLoc) + " at (" + str(self.x) + ", " + str(self.y) + ")"

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def change_sprite2(self, sprite):
        self.image = pygame.transform.smoothscale(sprite, (self.width, self.width))

    def change_sprite(self, rect):
        self.spriteLoc = [rect.left, rect.top]
        image = self.spritesheet.subsurface(rect).copy()
        self.image = pygame.transform.smoothscale(image, (self.width, self.width))