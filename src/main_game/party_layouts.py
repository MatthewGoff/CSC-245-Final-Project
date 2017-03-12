# Friends and enemies for the levels are hardcoded

import pygame

from party import Party
from player import Player
from abilities.fireball import Fireball
from abilities.energize import Energize
from abilities.heal import Heal
from abilities.power_attack import PowerAttack

class PartyTracker:
    def __init__(self):
        self.party_data = {}

    def get_parties(self, name, campaign, battle_listener):
        parties = []
        if name in self.party_data:
            parties = self.party_data[name]
        else:
            parties = self.init(name, campaign, battle_listener)
        return parties

    def init(self, name, campaign, battle_listener):
        parties = []
        if name == "olin107":
            parties = self.olin107(campaign, battle_listener)
        elif name == "olinhallway":
            parties = self.olinhallway(campaign, battle_listener)
        return parties


    def olin107(self, campaign, battle_listener):
        enemy_image = pygame.image.load("../assets/images/OtherSheet.png").convert_alpha()
        enemy_rect = pygame.Rect(2016, 224, 32, 32)
        enemy_image = enemy_image.subsurface(enemy_rect).copy()
        enemy_party = Party((90, 460),
                      32,
                      (32, 32),
                      enemy_image,
                      campaign.world,
                      battle_listener)
        enemy1 = Player(550, 200, 68, 98, "../assets/images/OtherSheet.png", 2016, 224, 32, 32, False)
        enemy2 = Player(550, 50, 68, 98, "../assets/images/OtherSheet.png", 2016, 224, 32, 32, False)
        enemy_party.members += [enemy1, enemy2]
        campaign.enemy = enemy_party
        campaign.world.add_party(enemy_party)

        player_image = pygame.image.load("../assets/images/player.png").convert_alpha()
        player_rect = pygame.Rect(0, 0, 48, 48)
        player_image = player_image.subsurface(player_rect).copy()
        user = Party(campaign.world.get_border().center,
                     32,
                     (10, 10),
                     player_image,
                     campaign.world,
                     battle_listener)
        campaign.user = user
        player = Player(20, 200, 68, 98, "../assets/images/player.png", 384, 0, 38, 48, True)
        player.abilities = [Energize(), Fireball(0, 0, 0), PowerAttack(), Heal()]
        player.change_hp(100)
        campaign.user.members += [player]
        campaign.world.add_party(user)

    def olinhallway(self, campaign, battle_listener):
        enemy_image = pygame.image.load("../assets/images/OtherSheet.png").convert_alpha()
        enemy_rect = pygame.Rect(2016, 224, 32, 32)
        enemy_image = enemy_image.subsurface(enemy_rect).copy()
        enemy_party = Party((532, 540),
                      32,
                      (32, 32),
                      enemy_image,
                      campaign.world,
                      battle_listener)
        enemy1 = Player(550, 200, 68, 98, "../assets/images/OtherSheet.png", 2016, 224, 32, 32, False)
        enemy1.change_hp(100)
        enemy_party.members += [enemy1]
        enemy_party2 = Party((320, 400),
                            32,
                            (32, 32),
                            enemy_image,
                            campaign.world,
                            battle_listener)
        enemy1 = Player(550, 200, 68, 98, "../assets/images/OtherSheet.png", 2016, 224, 32, 32, False)
        enemy2 = Player(550, 200, 68, 98, "../assets/images/OtherSheet.png", 2016, 224, 32, 32, False)
        enemy3 = Player(550, 200, 68, 98, "../assets/images/OtherSheet.png", 2016, 224, 32, 32, False)
        enemies = [enemy1, enemy2, enemy3]
        for e in enemies:
            e.change_hp(-30)
        enemy_party2.members += enemies
        parties = [enemy_party, enemy_party2]
        self.party_data["olinhallway"] = parties
        return parties


    def save_world_state(self, world):
        self.party_data[world.name] = world.parties
