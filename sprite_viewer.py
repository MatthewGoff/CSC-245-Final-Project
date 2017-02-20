
import pygame

class SpriteViewer:
    color = pygame.color.Color("LightGrey")
    color2 = pygame.color.Color("Red")
    curr_index = 0

    def __init__(self, x, y, width, height, spritesheet, tile_width):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tile_width = tile_width
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.sprites = []
        for i in range(spritesheet.get_width()/tile_width):
            for j in range(spritesheet.get_height()/tile_width):
                rect = pygame.Rect(i*tile_width, j*tile_width, tile_width, tile_width)
                image = spritesheet.subsurface(rect).copy()
                self.sprites += [pygame.transform.smoothscale(image, (tile_width, tile_width))]



    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        image = pygame.Surface([self.width/2 + 4, self.width/2 + 4])
        image.fill(self.color2)
        window.blit(image, (self.width/4 - 2, self.height/2-self.width/4 - 2))

        window.blit(pygame.transform.smoothscale(self.sprites[self.curr_index],
                                                 (self.width/2,self.width/2)), (self.width/4, self.height/2-self.width/4))
        if self.curr_index > 0:
            window.blit(pygame.transform.smoothscale(self.sprites[self.curr_index - 1], (self.width / 2, self.width / 2)),
                        (self.width / 4, self.height / 4 - self.width / 4))
        if self.curr_index < len(self.sprites) - 1:
            window.blit(pygame.transform.smoothscale(self.sprites[self.curr_index + 1], (self.width / 2, self.width / 2)),
                        (self.width / 4, (self.height - self.height / 4) - self.width / 4))

    def get_sprite(self):
        return self.sprites[self.curr_index]