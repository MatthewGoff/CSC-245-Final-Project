# Make pop-up "windows" that support text and dialogue boxes
# Author: Caleb
# Vers: winter 2017

import pygame

from button import Button

BORDER = 4
BORDER_COLOR = "Black"

class Prompt:

    def __init__(self, x, y, width, height, bg_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height))
        self.surface.fill(pygame.color.Color(BORDER_COLOR))
        self.subsurface = pygame.Surface((width - BORDER*2, height-BORDER*2))
        self.subsurface.fill(pygame.color.Color(bg_color))
        self.curr_line_y = 0
        self.buttons = []

    # In case we want to get fancy and allow movable prompts
    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # Internal use only
    # Check if word can fit on line
    # If not, save the current line to the list and start a new line
    # Add word to line
    def add_word(self, word, font, color, line, line_width, lines):
        word_img = font.render(" " + word, True, pygame.color.Color(color))
        if line == "":
            line = line + word
        elif line_width + word_img.get_width() > self.subsurface.get_width():
            line_img = font.render(line, True, pygame.color.Color(color))
            self.add_line(line_img, lines)
            line = word
        else:
            line = line + " " + word
        return line

    # Internal use only
    # Add line to list
    # Increment line
    def add_line(self, line_img, lines):
        lines += [(line_img,
                   self.curr_line_y)]
        self.curr_line_y += line_img.get_height()

    # Draw a line of text to the screen,
    # given a tuple containing that line and its y-position
    def draw_line(self, line_tuple, centered):
        line = line_tuple[0]
        y = line_tuple[1]
        if centered:
            x = self.subsurface.get_width()/2 - line.get_width()/2
        else:
            x = 0
        self.subsurface.blit(line, (x, y))

    # Add a given string to the prompt,
    # Formatted as specified
    def add_text(self, string, font, font_size, centered, color):
        font = pygame.font.SysFont(font, font_size)
        lines = []
        words = string.split(" ")
        line = ""
        line_width = 0
        line_img = None
        # Go through and split input string into lines of correct width
        while len(words) > 0:
            word = words[0]
            # Add word adds the line if it needs to start a new one
            line = self.add_word(word, font, color, line, line_width, lines)
            words.pop(0)
            line_img = font.render(line, True, pygame.color.Color(color))
            line_width = line_img.get_width()
        # Add final line
        if line_img is not None:
            self.add_line(line_img, lines)
        # Blit each line to prompt individually
        for line_tuple in lines:
            self.draw_line(line_tuple, centered)

    def draw(self, window):
        self.surface.blit(self.subsurface, (BORDER, BORDER))
        window.blit(self.surface, (self.x, self.y))

    def add_button(self, text, font_size, x, y, width, height, action):
        rect = pygame.Rect(x, y, width, height)
        button = Button(rect, font_size, text, action)
        self.buttons += [button]
        button.draw(self.subsurface)

    # Add height pixels of vertical space
    def v_space(self, height):
        self.curr_line_y += height

    def check_collisions(self, mouse_pos):
        adj_pos = (mouse_pos[0] - (self.x + BORDER), mouse_pos[1] - (self.y + BORDER))
        clicked_buttons = [button for button in self.buttons if
                           button.rect.collidepoint(adj_pos)]
        #if clicked_buttons and clicked_buttons[0].action == exit:
            #pygame.quit()
        if clicked_buttons:
            return (True, clicked_buttons[0].action == exit)

'''Prompts. These will probably be moved eventually.'''
# Prompt for the battle class
def battle_start(native_screen_size):
    prompt = Prompt(native_screen_size[0]/2 - 200, native_screen_size[1]/2 - 150, 400, 300, "LightGrey")
    msg = "Welcome to the battle demo. Every round, each combatant will take his or her turn." \
               " When it's your turn, an ability bar will appear. Use the mouse to select an ability," \
               " then choose a target on which to use it."
    prompt.add_text(msg, "freesansbold.ttf", 25, False, "Black")
    prompt.v_space(20)
    prompt.add_text("When you're ready, press 'CONTINUE'.", "freesansbold.ttf", 25, True, "Blue")
    prompt.v_space(40)
    prompt.add_text("Good luck!", "freesansbold.ttf", 40, True, "Green")
    prompt.add_button("CONTINUE", 25,
                      prompt.subsurface.get_width()/2 - 50,
                      prompt.subsurface.get_height() - 40, 100, 40, "loof")
    return prompt

# Prompt for the campaign
def campaign_start(native_screen_size):

    prompt = Prompt(native_screen_size[0]/2 - 200, native_screen_size[1]/2 - 150, 400, 300, "DarkRed")
    msg = "On your way back to CSC 245 class from the bathroom," \
          " the earth begins to shake beneath your feet, with an audible rumble." \
          " You hurry back to class, but upon entering Olin 107, you find a room" \
          " bathed in blood, with no sign of your classmates or Matt." \
          " You hear moaning noises and irregular footsteps. Some kind of creature" \
          " or creatures must have done this! Find the source of evil and destroy it..."
    prompt.add_text(msg, "freesansbold.ttf", 25, True, "Black")
    prompt.v_space(15)
    prompt.add_text("...or are they already here??!", "freesansbold.ttf", 25, True, "Black")
    prompt.v_space(10)
    prompt.add_text("Use the WASD keys to navigate through Union College", "freesansbold.ttf", 20, True, "White")
    prompt.add_button("Begin Journey", 25,
                      prompt.subsurface.get_width() / 2 - 60,
                      prompt.subsurface.get_height() - 40, 120, 40, "loof")
    return prompt

def death(native_screen_size):
    prompt = Prompt(native_screen_size[0] / 2 - 200, native_screen_size[1] / 2 - 150, 400, 300, "DarkRed")
    msg = "You are dead."
    prompt.add_text(msg, "freesansbold.ttf", 25, True, "Black")
    prompt.v_space(15)
    prompt.add_text("GAME OVER", "freesansbold.ttf", 25, True, "Black")
    prompt.add_button("Oh well", 25,
                      prompt.subsurface.get_width() / 2 - 60,
                      prompt.subsurface.get_height() - 40, 120, 40, "loof")
    return prompt

def battle_won(native_screen_size):
    prompt = Prompt(native_screen_size[0] / 2 - 200, native_screen_size[1] / 2 - 150, 400, 300, "DarkRed")
    msg = "You won!"
    prompt.add_text(msg, "freesansbold.ttf", 25, True, "Black")
    prompt.v_space(15)
    prompt.add_text("EXTREMELY GOOD STUFF!", "freesansbold.ttf", 25, True, "Black")
    prompt.add_button("Exit", 25,
                      prompt.subsurface.get_width() / 2 - 60,
                      prompt.subsurface.get_height() - 40, 120, 40, exit)
    return prompt

def exit():
    pygame.quit()