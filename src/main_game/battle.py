# Class runs the game loop for Battle portion of the game
# Author: Caleb
# Vers: Winter 2017

import pygame, Queue, random
from player import Player
from ability_bar import AbilityBar
from abilities.fireball import Fireball
from abilities.energize import Energize
from abilities.heal import Heal
from abilities.power_attack import PowerAttack
from prompt import battle_start
from constants import NATIVE_SCREEN_SIZE


TURN_MSG = "Player Turn"
ABIL_BAR_HEIGHT = 60


class Battle:
    WINDOW_SIZE = (640, 480)

    def __init__(self, party1, party2, location, window, fullscreen):
        self.won = False
        self.spritesheet = pygame.image.load(
            "../assets/images/player.png").convert_alpha()
        self.window = window
        self.width = Battle.WINDOW_SIZE[0]
        self.height = Battle.WINDOW_SIZE[1]
        self.fullscreen = fullscreen
        self.pos = location
        if location == "demo":
            self.bg = pygame.image.load("../assets/images/battle_demo_bg.jpg").convert_alpha()
            self.bg = pygame.transform.smoothscale(self.bg, (self.window.get_width(), self.window.get_height()))
        self.party1 = party1
        self.party2 = party2
        self.friendlies = party1#.members
        self.enemies = party2#.members
        self.friendly_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.bars = pygame.sprite.Group()
        self.font = pygame.font.SysFont("monospace", 25)
        self.turn_msg =  self.font.render(TURN_MSG, 0, (0, 0, 0))
        combatants = Queue.PriorityQueue()
        self.place_combatants(self.friendlies, self.enemies, combatants)
        self.ability_bar = AbilityBar(0, self.height - ABIL_BAR_HEIGHT, self.width, ABIL_BAR_HEIGHT, self.abilities)
        self.combatants = []
        for i in range(len(self.friendlies)+len(self.enemies)):
            self.combatants.append(combatants.get()[1])
        self.curr_combatant = -1
        self.next_turn()
        self.in_prompt = True
        self.prompt = battle_start((window.get_width(), window.get_height()))

    def place_combatants(self, friends, enemies, p_queue):
        n = 1
        for p in friends:
            p.set_pos(self.width / 8, n * (self.height / (len(friends) + 1)))
            p_queue.put((p.speed, p))
            self.friendly_sprites.add(p)
            self.friendly_sprites.add(p.hp)
            self.friendly_sprites.add(p.energy)
            self.bars.add(p.bar_bg)
            if p.is_human:
                self.abilities = p.abilities
            n += 1
        n = 1
        for p in enemies:
            p.set_pos(self.width - p.width - self.width / 8, n * (self.height / (len(enemies) + 1)))
            p_queue.put((p.speed, p))
            self.enemy_sprites.add(p)
            self.enemy_sprites.add(p.hp)
            self.enemy_sprites.add(p.energy)
            self.bars.add(p.bar_bg)
            n += 1

    def draw_interface(self, window):
        window.blit(self.turn_msg, (self.width/2 - self.turn_msg.get_width()/2, 0))
        self.ability_bar.draw(window)


    def handle_events(self):
        keep_going = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
            elif self.in_prompt:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_pressed = event.dict['button']
                    mouse_pos = event.dict['pos']
                    if button_pressed == 1 and self.prompt.check_collisions(mouse_pos):
                        self.in_prompt = False
            elif event.type == pygame.KEYDOWN:
                key_pressed = event.dict['key'] % 256
                if key_pressed == pygame.K_ESCAPE:
                    if self.fullscreen:
                        pygame.display.set_mode(Battle.WINDOW_SIZE)
                        self.fullscreen = False
                    else:
                        pygame.display.set_mode(Battle.WINDOW_SIZE,
                                                pygame.FULLSCREEN)
                        self.fullscreen = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print "Button pressed:", event.dict['button'], "@", event.dict['pos']
                button_pressed = event.dict['button']
                target = event.dict['pos']

                if button_pressed == 1 and self.player_turn:
                    self.click(target)
        return keep_going

    def next_turn(self):
        if self.curr_combatant == len(self.combatants) - 1:
            self.curr_combatant = 0
        else:
            self.curr_combatant += 1
        if self.combatants[self.curr_combatant].is_human:
            self.player_turn = True
        else:
            self.player_turn = False

    # Selects the ability the mouse is over, or attacks the enemy the mouse is over with the selected ability
    def click(self, pos):
        self.ability_bar.click_ability(pos)
        valid_targets = self.ability_bar.get_valid_targets(self.friendlies, self.enemies)
        target = None
        for t in valid_targets:
            if t.rect.collidepoint(pos):
                target = t
        player = self.combatants[self.curr_combatant]
        if not target is None and player.can_use(self.ability_bar.selected_ability, target):
            player.use_ability(self.ability_bar.selected_ability, target)
            self.next_turn()

    # Attacks random opponent
    def ai_turn(self):
        if not self.player_turn:
            curr_combatant = self.combatants[self.curr_combatant]
            pygame.time.wait(1000)

            if self.friendlies.count(curr_combatant) > 0:
                if curr_combatant.hp.curr < .25*curr_combatant.hp.max and curr_combatant.can_use(Heal, curr_combatant):
                    curr_combatant.use_ability(Heal, curr_combatant)
                else:
                    rand_index = random.randint(0, len(self.enemies)-1)
                    curr_combatant.attack(self.enemies[rand_index])
                self.next_turn()
            else:
                if curr_combatant.hp.curr < .25*curr_combatant.hp.max and curr_combatant.can_use(Heal, curr_combatant):
                    curr_combatant.use_ability(Heal, curr_combatant)
                else:
                    rand_index = random.randint(0, len(self.friendlies) - 1)
                    curr_combatant.attack(self.friendlies[rand_index])
                self.next_turn()

    # Will use to animate, probably
    def simulate(self):
        pass

    # Gets rids of dead combatants and checks for win
    def apply_rules(self):
        keep_going = True
        for p in self.friendlies:
            if p.dead:
                if p.is_human:
                    self.player_turn = False
                self.friendlies.remove(p)
                self.combatants.remove(p)
                self.friendly_sprites.remove(p)
                self.friendly_sprites.remove(p.hp)
                self.friendly_sprites.remove(p.energy)
                self.bars.remove(p.bar_bg)

        for p in self.enemies:
            if p.dead:
                self.enemies.remove(p)
                self.combatants.remove(p)
                self.enemy_sprites.remove(p)
                self.enemy_sprites.remove(p.hp)
                self.enemy_sprites.remove(p.energy)
                self.bars.remove(p.bar_bg)

        if self.curr_combatant >= len(self.combatants):
            self.curr_combatant = 0

        if len(self.friendlies) == 0:
            keep_going = False
        elif len(self.enemies) == 0:
            self.won = True
            keep_going = False

        return keep_going

    def draw(self, window):
        # Fill BG
        window.blit(self.bg, (0,0))
            #fill(pygame.color.Color("grey"))
        # Draw combatants
        self.bars.draw(window)
        self.friendly_sprites.draw(window)
        self.enemy_sprites.draw(window)
        if self.in_prompt:
            self.prompt.draw(window)
        elif self.player_turn:
            self.draw_interface(window)
        # Swap display
        pygame.display.update()

    def end_battle(self):
        if self.won:
            print "Battle Won :)"
        else:
            print "Battle Lost :("

    def quit(self):
        pygame.quit()

    def run(self):
        frame_rate = 60
        tick_time = int(1.0 / frame_rate * 1000)

        # The game loop starts here.

        running = True
        while running:
            pygame.time.wait(tick_time)

            # 1. Apply rules
            running = self.apply_rules()
            # 2. AI turn
            if running and not self.in_prompt:
                self.ai_turn()

            # 3. Handle events.
            if running:
                running = self.handle_events()

            # 4. Draw frame
            self.draw(self.window)

        return self.won


def demo(window):
    pygame.display.set_mode(Battle.WINDOW_SIZE, pygame.FULLSCREEN)
    player = Player(20, 200, 68, 98, "../assets/images/player.png", 384, 0, 38, 48, True)
    player.abilities = [Energize(), Fireball(0,0,0), PowerAttack(), Heal()]
    friend = Player(20, 350, 68, 98, "../assets/images/player.png", 384, 0, 38, 48, False)
    enemy = Player(550, 200, 68, 98, "../assets/images/OtherSheet.png",2016, 224, 32, 32, False)
    enemy2 = Player(550, 50, 68, 98, "../assets/images/OtherSheet.png", 2016, 224, 32, 32, False)
    battle = Battle([player, friend], [enemy, enemy2], "demo", window, False)
    return battle.run()

