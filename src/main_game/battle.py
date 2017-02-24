# Class runs the game loop for Battle portion of the game

import pygame, Queue, random
from player import Player

class Battle:

    WIDTH = 640
    HEIGHT = 480

    def __init__(self, party1, party2, location, window, fullscreen):
        self.won = False
        self.spritesheet = pygame.image.load(
            "../assets/images/player.png").convert_alpha()
        self.window = window
        self.width = window.get_width()
        self.height = window.get_height()
        self.fullscreen = fullscreen
        self.pos = location
        self.party1 = party1
        self.party2 = party2
        self.friendlies = party1#.members
        self.enemies = party2#.members
        self.friendly_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.bars = pygame.sprite.Group()
        combatants = Queue.PriorityQueue()
        self.place_combatants(self.friendlies, self.enemies, combatants)
        self.combatants = []
        for i in range(len(self.friendlies)+len(self.enemies)):
            self.combatants.append(combatants.get()[1])
        self.curr_combatant = -1
        self.next_turn()

    def place_combatants(self, friends, enemies, p_queue):
        n = 1
        for p in friends:
            p.set_pos(self.width / 8, n * (self.height / (len(friends) + 1)))
            p_queue.put((p.speed, p))
            self.friendly_sprites.add(p)
            self.friendly_sprites.add(p.hp)
            self.friendly_sprites.add(p.energy)
            self.bars.add(p.bar_bg)
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



    def handle_events(self):
        keep_going = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
            elif event.type == pygame.KEYDOWN:
                key_pressed = event.dict['key'] % 256
                if key_pressed == pygame.K_ESCAPE:
                    if self.fullscreen:
                        pygame.display.set_mode((self.width,
                                                 self.height))
                        self.fullscreen = False
                    else:
                        pygame.display.set_mode((self.width,
                                                 self.height),
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
        if self.combatants[self.curr_combatant].is_player:
            self.player_turn = True
        else:
            self.player_turn = False

    # If clicked on an enemy, attack that enemy
    def click(self, pos):
        enemy = None
        for e in self.enemies:
            if e.rect.collidepoint(pos):
                enemy = e
        if not enemy is None:
            self.combatants[self.curr_combatant].attack(enemy)
            self.next_turn()

    # Attacks random opponent
    def ai_turn(self):
        if not self.player_turn:
            curr_combatant = self.combatants[self.curr_combatant]
            pygame.time.wait(1000)

            if self.friendlies.count(curr_combatant) > 0:
                rand_index = random.randint(0, len(self.enemies)-1)
                curr_combatant.attack(self.enemies[rand_index])
                self.next_turn()
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
                if p.is_player:
                    self.player_turn = False
                self.friendlies.remove(p)
                self.combatants.remove(p)
                self.friendly_sprites.remove(p)

        for p in self.enemies:
            if p.dead:
                self.enemies.remove(p)
                self.combatants.remove(p)
                self.enemy_sprites.remove(p)

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
        window.fill(pygame.color.Color("grey"))
        # Draw combatants
        self.bars.draw(window)
        self.friendly_sprites.draw(window)
        self.enemy_sprites.draw(window)
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
            if running:
                self.ai_turn()

            # 3. Handle events.
            if running:
                running = self.handle_events()

            # 4. Draw frame
            self.draw(self.window)

            # 5. Check for endgame
            if not running:
                self.end_battle()

        self.quit()

my_win = pygame.display.set_mode((640, 480))
player = Player(20, 200, 68, 98, "../assets/images/player.png", 53, 96, 34, 49, True)
friend = Player(20, 350, 68, 98, "../assets/images/player.png", 53, 96, 34, 49, False)
enemy = Player(550, 200, 68, 98, "../assets/images/player.png", 57, 48, 34, 49, False)
enemy2 = Player(550, 50, 68, 98, "../assets/images/player.png", 57, 48, 34, 49, False)
battle = Battle([player, friend], [enemy, enemy2], (0, 0), my_win, False)
battle.run()