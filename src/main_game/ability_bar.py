# UI for choosing abilities (might be a placeholder; graphics certainly are)
# Author: Caleb
# "Winter" 2017

import pygame

NUM_ABILITIES = 4
PADDING = 10
ICON_SIZE = 40
SELECTOR_COLOR = "Blue"

class AbilityBar:
    def __init__(self, x, y, width, height, abilities):
        self.abilities = abilities
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        spritesheet = pygame.image.load("../assets/images/OtherSheet.png").convert_alpha()
        sprite_rect = pygame.Rect(1696, 0, 32, 32)
        image = spritesheet.subsurface(sprite_rect).copy()
        self.image = pygame.transform.smoothscale(image, (width, height))
        self.selected_ability = None
        self.selector = pygame.Surface((ICON_SIZE + 4, ICON_SIZE + 4))
        self.selector.fill(pygame.color.Color(SELECTOR_COLOR))

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        x = self.x + self.width/2 - (NUM_ABILITIES*ICON_SIZE + (NUM_ABILITIES - 1)*PADDING)/2
        for i in range(NUM_ABILITIES):
            if self.abilities[i] is self.selected_ability:
                window.blit(self.selector, (x - 2, self.y + PADDING - 2))
            self.abilities[i].draw_icon(x, self.y + PADDING, window)
            x += ICON_SIZE + PADDING

    def click_ability(self, pos):
        x, y = pos[0], pos[1]
        left_bound = self.x + self.width/2 - (NUM_ABILITIES*ICON_SIZE + (NUM_ABILITIES - 1)*PADDING)/2
        right_bound = self.x + self.width/2 + (NUM_ABILITIES*ICON_SIZE + (NUM_ABILITIES - 1)*PADDING)/2
        top_bound = self.y + PADDING
        bot_bound = self.y + self.height - PADDING
        if x > left_bound and x < right_bound and y > top_bound and y < bot_bound:
            self.selected_ability = self.abilities[(x - left_bound)/(ICON_SIZE + PADDING)]

    def get_valid_targets(self, friends, enemies):
        valid_targets = []
        if self.selected_ability is not None and self.selected_ability.friends_usable:
            valid_targets += friends
        if self.selected_ability is not None and self.selected_ability.enemies_usable:
            valid_targets += enemies
        return valid_targets

