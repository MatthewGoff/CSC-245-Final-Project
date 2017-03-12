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

    def get_parties(self, name):
        parties = []
        if name in self.party_data:
            parties = self.party_data[name]
        return parties

    def init_olin107(self, campaign, battle_listener):
        enemy_image = pygame.image.load("../assets/images/OtherSheet.png").convert_alpha()
        enemy_rect = pygame.Rect(2016, 224, 32, 32)
        enemy_image = enemy_image.subsurface(enemy_rect).copy()
        enemy = Party((90, 460),
                      32,
                      (32, 32),
                      enemy_image,
                      campaign.world,
                      battle_listener)
        enemy1 = Player(550, 200, 68, 98, "../assets/images/OtherSheet.png", 2016, 224, 32, 32, False)
        enemy2 = Player(550, 50, 68, 98, "../assets/images/OtherSheet.png", 2016, 224, 32, 32, False)
        enemy.members += [enemy1, enemy2]
        campaign.enemy = enemy
        campaign.world.add_party(enemy)

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

    def save_world_state(self, world):
        self.party_data[world.name] = world.parties
