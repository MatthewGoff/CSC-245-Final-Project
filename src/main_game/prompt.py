# Make pop-up "windows" that support text and dialogue boxes
# Author: Caleb
# Vers: winter 2017

import pygame

from button import Button
from util import TextInputBox
from constants import TILE_WIDTH

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
        self.text_boxes = []
        self.output_dict = {}
        self.active_text_box = None

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

    def add_text_by_pos(self, string, font, font_size, color, x, y):
        font = pygame.font.SysFont(font, font_size)
        txt = font.render(string, True, pygame.color.Color(color))
        self.subsurface.blit(txt, (x,y))


    def handle_keydown(self, key_pressed):
        # Cycle through the text input boxes in the prompt
        if key_pressed == pygame.K_TAB or key_pressed == pygame.K_RETURN:
            if self.active_text_box is not None:
                index = self.text_boxes.index(self.active_text_box)
                if index + 1 == len(self.text_boxes):
                    index = -1
                self.active_text_box.deselect()
                self.active_text_box = self.text_boxes[index + 1]
                self.active_text_box.select()
        # Make the active box handle input
        elif self.active_text_box is not None:
            self.active_text_box.handle_keydown(key_pressed)

    def draw(self, window):
        for box in self.text_boxes:
            box.draw(self.subsurface)
        self.surface.blit(self.subsurface, (BORDER, BORDER))
        window.blit(self.surface, (self.x, self.y))

    def add_button(self, text, font_size, x, y, width, height, action):
        rect = pygame.Rect(x, y, width, height)
        button = Button(rect, font_size, text, action)
        self.buttons += [button]
        button.draw(self.subsurface)

    # Key refers to the text box's corresponding key in the output dictionary
    def add_text_box(self, x, y, width, key):
        box = TextInputBox(x, y, width, key, self.output_dict)
        self.text_boxes += [box]

    # Add height pixels of vertical space
    def v_space(self, height):
        self.curr_line_y += height

    # For debugging
    def print_output(self):
        print str(self.output_dict)

    # Returns the object the user clicked on
    def check_collisions(self, mouse_pos):
        clicked_obj = None
        adj_pos = (mouse_pos[0] - (self.x + BORDER), mouse_pos[1] - (self.y + BORDER))
        clicked_buttons = [button for button in self.buttons if
                           button.rect.collidepoint(adj_pos)]
        clicked_txt_boxes = [box for box in self.text_boxes if
                           box.rect.collidepoint(adj_pos)]
        if clicked_buttons:
            clicked_obj = clicked_buttons[0]
        elif clicked_txt_boxes:
            if self.active_text_box is not None:
                self.active_text_box.deselect()
            clicked_txt_boxes[0].select()
            self.active_text_box = clicked_txt_boxes[0]
            clicked_obj = clicked_txt_boxes[0]
        return clicked_obj

'''Prompts. These will probably be moved eventually.'''
# Prompt for the battle class
def battle_start(native_screen_size):
    prompt = Prompt(native_screen_size[0]/2 - 200,
                    native_screen_size[1]/2 - 150,
                    400,
                    300,
                    "DarkBlue")
    msg = "Ah, the thrill of battle! Every round, each combatant will take his or her turn." \
               " When it's your turn, an ability bar will appear." \
          " Use the mouse to select an ability," \
               " then choose a target on which to use it. Be careful, abilities cost resources," \
          "so be strategic."
    prompt.add_text(msg, "freesansbold.ttf", 25, False, "White")
    prompt.v_space(20)
    prompt.add_text("When you're ready, press 'CONTINUE'.", "freesansbold.ttf", 25, True, "White")
    prompt.v_space(40)
    prompt.add_text("Good luck!", "freesansbold.ttf", 40, True, "White")
    prompt.add_button("CONTINUE", 25,
                      prompt.subsurface.get_width()/2 - 50,
                      prompt.subsurface.get_height() - 40, 100, 40, "beef")
    return prompt

# Prompt for the campaign
def campaign_start(native_screen_size):

    prompt = Prompt(native_screen_size[0]/2 - 200,
                    native_screen_size[1]/2 - 150,
                    400, 325, "DarkRed")
    msg = "On your way back to CSC 245 class from the bathroom," \
          " the earth begins to shake beneath your feet, with an audible rumble." \
          " You hurry back to class, but upon entering Olin 107, you find a room" \
          " bathed in blood, with no sign of your classmates or Matt." \
          " You hear moaning noises and irregular footsteps. Some kind of creature" \
          " or creatures must have done this! Find the source of evil and destroy it." \
          " Save Union College!"
    prompt.add_text(msg, "freesansbold.ttf", 25, True, "Black")
    prompt.v_space(15)
    prompt.add_text("The footsteps get closer. This can't be good.",
                    "freesansbold.ttf", 25, True, "Black")
    prompt.v_space(10)
    prompt.add_text("Use the WASD keys to navigate through Union College",
                    "freesansbold.ttf", 20, True, "White")
    prompt.add_text("Use the scoll wheel to zoom in and out",
                    "freesansbold.ttf", 20, True, "White")
    prompt.add_button("Begin Journey", 25,
                      prompt.subsurface.get_width() / 2 - 70,
                      prompt.subsurface.get_height() - 40, 140, 40, "okay")
    return prompt

# Game over death prompt (closes game, currently)
def death(native_screen_size):
    prompt = Prompt(native_screen_size[0] / 2 - 200,
                    native_screen_size[1] / 2 - 150,
                    400, 300, "DarkRed")
    msg = "You are dead."
    prompt.add_text(msg, "freesansbold.ttf", 25, True, "Black")
    prompt.v_space(15)
    prompt.add_text("GAME OVER", "freesansbold.ttf", 25, True, "Black")
    prompt.add_button("Restart", 25,
                      prompt.subsurface.get_width() / 2 - 130,
                      prompt.subsurface.get_height() - 40, 120, 40, "restart")
    prompt.add_button("Exit", 25,
                      prompt.subsurface.get_width() / 2 + 10,
                      prompt.subsurface.get_height() - 40, 120, 40, "exit")
    return prompt

# Post-battle message. The button resumes the campaign
def battle_won(native_screen_size):
    prompt = Prompt(native_screen_size[0] / 2 - 200,
                    native_screen_size[1] / 2 - 150,
                    400, 300, "DarkRed")
    msg = "Well fought! but that wasn't the last of them."
    prompt.add_text(msg, "freesansbold.ttf", 25, True, "Black")
    prompt.v_space(15)
    prompt.add_text("Be careful out there!", "freesansbold.ttf", 25, True, "Black")
    prompt.add_button("Continue", 25,
                      prompt.subsurface.get_width() / 2 - 60,
                      prompt.subsurface.get_height() - 40, 120, 40, "okay")
    return prompt

# A demo for text input
def input_example(native_screen_size):
    prompt = Prompt(native_screen_size[0] / 2 - 200,
                    native_screen_size[1] / 2 - 150,
                    400, 300, "DarkRed")
    msg = "Input Demo"
    prompt.add_text(msg, "freesansbold.ttf", 30, True, "Black")
    msg = "Please enter stats for the first player"
    prompt.add_text(msg, "freesansbold.ttf", 25, True, "Black")
    prompt.v_space(15)
    msg = "Press ENTER while in prompt to print output to console. " \
          "You can click to select boxes, or tab through them."
    prompt.add_text(msg, "freesansbold.ttf", 20, True, "Black")
    prompt.v_space(15)
    prompt.add_text_by_pos("strength:",
                           "freesansbold.ttf", 20, "Black", 10, prompt.curr_line_y)
    prompt.add_text_by_pos("stamina:",
                           "freesansbold.ttf", 20, "Black", 10, prompt.curr_line_y + 20)
    prompt.add_text_by_pos("intellect:",
                           "freesansbold.ttf", 20, "Black", 10, prompt.curr_line_y + 40)
    prompt.add_text_box(80, prompt.curr_line_y, 160, "str")
    prompt.add_text_box(80, prompt.curr_line_y + 20, 160, "stam")
    prompt.add_text_box(80, prompt.curr_line_y + 40, 160, "int")
    prompt.add_button("Continue", 25,
                      prompt.subsurface.get_width() / 2 - 60,
                      prompt.subsurface.get_height() - 40, 120, 40, "okay")
    return prompt

# Prompt that appears in editor when placing a door,
# so the user can specify to where the door leads
def door_placement(win_w, win_h, loc, fg):
    prompt = Prompt(win_w / 2 - 200, win_h / 2 - 150, 400, 300, "DarkRed")
    prompt.output_dict["column"] = loc[0]
    prompt.output_dict["row"] = loc[1]
    prompt.output_dict["fg"] = fg
    msg = "New Door"
    prompt.add_text(msg, "freesansbold.ttf", 30, True, "Black")
    msg = "Please enter the attributes for the door"
    prompt.add_text(msg, "freesansbold.ttf", 25, True, "Black")
    prompt.v_space(15)
    prompt.add_text_by_pos("world:",
                           "freesansbold.ttf", 20, "Black", 10, prompt.curr_line_y)
    prompt.add_text_by_pos("start x:",
                           "freesansbold.ttf", 20, "Black", 10, prompt.curr_line_y + 20)
    prompt.add_text_by_pos("start y:",
                           "freesansbold.ttf", 20, "Black", 10, prompt.curr_line_y + 40)
    prompt.add_text_box(80, prompt.curr_line_y, 160, "world")
    prompt.add_text_box(80, prompt.curr_line_y + 20, 160, "x")
    prompt.add_text_box(80, prompt.curr_line_y + 40, 160, "y")
    prompt.add_button("Place", 25,
                      prompt.subsurface.get_width() / 2 - 60,
                      prompt.subsurface.get_height() - 40, 120, 40, "door")
    return prompt

# In progress/draft
def party_placement(win_w, win_h, loc, player_num):
    prompt = Prompt(win_w / 2 - 200, win_h / 2 - 150, 400, 300, "DarkRed")
    prompt.output_dict["x"] = loc[0]
    prompt.output_dict["y"] = loc[1]
    msg = "New Door"
    prompt.add_text(msg, "freesansbold.ttf", 30, True, "Black")
    msg = "Please enter the attributes for the door"
    prompt.add_text(msg, "freesansbold.ttf", 25, True, "Black")
    prompt.v_space(15)
    prompt.add_text_by_pos("world:",
                           "freesansbold.ttf", 20, "Black", 10, prompt.curr_line_y)
    prompt.add_text_by_pos("start x:",
                           "freesansbold.ttf", 20, "Black", 10, prompt.curr_line_y + 20)
    prompt.add_text_by_pos("start y:",
                           "freesansbold.ttf", 20, "Black", 10, prompt.curr_line_y + 40)
    prompt.add_text_box(80, prompt.curr_line_y, 160, "world")
    prompt.add_text_box(80, prompt.curr_line_y + 20, 160, "x")
    prompt.add_text_box(80, prompt.curr_line_y + 40, 160, "y")
    prompt.add_button("Place", 25,
                      prompt.subsurface.get_width() / 2 - 60,
                      prompt.subsurface.get_height() - 40, 120, 40, "door")
    return prompt

# prompt displayed on encountering the second party member
def meet_ally(native_screen_size, party):
    prompt = Prompt(native_screen_size[0] / 2 - 200,
                    native_screen_size[1] / 2 - 150,
                    400, 300, "DarkRed")
    msg = "Ally Encountered"
    prompt.add_text(msg, "freesansbold.ttf", 25, True, "Black")
    prompt.v_space(15)
    if len(party.members) == 2:
        msg = "Hi! I thought I might be the only one left." \
              " I'm trying to fight my way outside;" \
              " out there we stand a better shot of figuring out what's going on," \
              " or escaping at the very least!"
        prompt.add_text(msg, "freesansbold.ttf", 25, True, "Black")
    elif len(party.members) == 3:
        prompt.v_space(15)
        prompt.add_text("Thanks for freeing me! I'll help you fight... whatever that thing is.",
                        "freesansbold.ttf", 25, True, "Black")
    prompt.add_button("Welcome!", 25,
                      prompt.subsurface.get_width() / 2 - 60,
                      prompt.subsurface.get_height() - 40, 120, 40, "okay")
    return prompt

def olin_outside(native_screen_size):
    prompt = Prompt(native_screen_size[0] / 2 - 200,
                    native_screen_size[1] / 2 - 150,
                    400, 300, "DarkRed")
    msg = "Out here, you try to get your bearings."
    prompt.add_text(msg, "freesansbold.ttf", 25, True, "Black")
    prompt.v_space(15)
    prompt.add_text("The ground trembles again; it seems to come from the Nott Memorial!",
                    "freesansbold.ttf", 25, True, "Black")
    prompt.add_button("Continue", 25,
                      prompt.subsurface.get_width() / 2 - 60,
                      prompt.subsurface.get_height() - 40, 120, 40, "okay")
    return prompt