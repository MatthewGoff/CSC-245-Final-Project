# Friends and enemies for the levels are hardcoded

import pygame

from party import Party
from combatant import Combatant
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
        elif name == "nott_interior":
            parties = self.nott_interior(campaign, battle_listener)
        return parties


    def olin107(self, campaign, battle_listener):
        enemy_image = pygame.image.load("../assets/images/zombie.png").convert_alpha()
        enemy_rect = pygame.Rect(48, 0, 48, 48)
        enemy_image = enemy_image.subsurface(enemy_rect).copy()
        enemy_party = Party((90, 460),
                      48,
                      (48, 48),
                      enemy_image,
                      campaign.world,
                      battle_listener)
        enemy1 = Combatant(550, 200, 72, 72, "../assets/images/zombie.png", 48 * 4, 0, 48, 48, False)
        enemy2 = Combatant(550, 50, 72, 72, "../assets/images/zombie_magic.png", 48 * 5, 0, 48, 48, False)
        enemy_party.members += [enemy1, enemy2]
        campaign.enemy = enemy_party
        campaign.world.add_party(enemy_party)

        player_image = pygame.image.load("../assets/images/player.png").convert_alpha()
        player_rect = pygame.Rect(0, 0, 48, 48)
        player_image = player_image.subsurface(player_rect).copy()
        user = Party(campaign.world.get_border().center,
                     48,
                     (10, 25),
                     player_image,
                     campaign.world,
                     battle_listener)
        user.make_friendly()
        user.make_controllable("../assets/images/player.png")
        campaign.user = user
        player = Combatant(20, 200, 72, 72, "../assets/images/player.png", 384, 0, 48, 48, True)
        player.abilities = [Energize(), Fireball(0, 0, 0), PowerAttack(), Heal()]
        player.change_hp(100)
        campaign.user.members += [player]
        campaign.world.add_party(user)

    def olinhallway(self, campaign, battle_listener):
        enemy_image = pygame.image.load("../assets/images/zombie2.png").convert_alpha()
        enemy_rect = pygame.Rect(48, 0, 48, 48)
        enemy_image = enemy_image.subsurface(enemy_rect).copy()
        enemy_party = Party((532, 540),
                      48,
                      (48, 48),
                      enemy_image,
                      campaign.world,
                      battle_listener)
        enemy1 = Combatant(550, 200, 72, 72, "../assets/images/zombie2.png", 48 * 4, 0, 48, 48, False)
        enemy1.change_hp(100)
        enemy_party.members += [enemy1]

        enemy_image = pygame.image.load("../assets/images/zombie_magic.png").convert_alpha()
        enemy_rect = pygame.Rect(48, 0, 48, 48)
        enemy_image = enemy_image.subsurface(enemy_rect).copy()
        enemy_party2 = Party((320, 400),
                            48,
                            (48, 48),
                            enemy_image,
                            campaign.world,
                            battle_listener)
        enemy1 = Combatant(550, 200, 72, 72, "../assets/images/zombie_magic.png", 48 * 4, 0, 48, 48, False)
        enemy2 = Combatant(550, 200, 72, 72, "../assets/images/zombie2.png", 48 * 4, 0, 48, 48, False)
        enemy3 = Combatant(550, 200, 72, 72, "../assets/images/zombie.png", 48 * 4, 0, 48, 48, False)
        enemies = [enemy1, enemy2, enemy3]
        for e in enemies:
            e.change_hp(-35)
        enemy_party2.members += enemies

        friend_image = pygame.image.load("../assets/images/player2.png").convert_alpha()
        friend_rect = pygame.Rect(48, 0, 48, 48)
        friend_image = friend_image.subsurface(friend_rect).copy()
        friend_party = Party((320, 500),
                             48,
                             (48, 48),
                              friend_image,
                             campaign.world,
                             battle_listener)
        friend = Combatant(550, 200, 72, 72, "../assets/images/player2.png", 48 * 7, 0, 48, 48, False)
        friend_party.members += [friend]
        friend_party.make_friendly()

        parties = [enemy_party, enemy_party2, friend_party]
        self.party_data["olinhallway"] = parties
        return parties

    def nott_interior(self, campaign, battle_listener):
        friend_image = pygame.image.load("../assets/images/player3.png").convert_alpha()
        friend_rect = pygame.Rect(48, 0, 48, 48)
        friend_image = friend_image.subsurface(friend_rect).copy()
        friend_party = Party((85, 290),
                             48,
                             (48, 48),
                             friend_image,
                             campaign.world,
                             battle_listener)
        friend = Combatant(550, 200, 72, 72, "../assets/images/player3.png", 48 * 7, 0, 48, 48, False)
        friend_party.members += [friend]
        friend_party.make_friendly()

        self.party_data["nott_interior"] = [friend_party]
        return [friend_party]

    def save_world_state(self, world):
        self.party_data[world.name] = world.parties
