from __future__ import print_function, division
from app.api import ClashAPI
from pprint import pprint


class PlayerData:
    def __init__(self, tag):
        self.player_tag = tag
        self.player_name = None
        self.town_hall_level = None
        self.current_trophies = None
        self.attack_wins = None
        self.defense_wins = None
        self.bestTrophies = None
        self.donations_given = None
        self.donations_received = None
        self.exp_level = None
        self.king_level = None
        self.queen_level = None
        self.warden_level = None
        self.battle_machine_Level = None
        self.war_stars = None
        self.get_player_info()

    def parse_hero_info(self, heroList):

        for hero in heroList:
            if hero['name'] == 'Barbarian King':
                self.king_level = hero.get('level')
            elif hero['name'] == 'Battle Machine':
                self.battle_machine_Level = hero.get('level')
            elif hero['name'] == 'Archer Queen':
                self.queen_level = hero.get('level')
            elif hero['name'] == 'Grand Warden':
                self.warden_level = hero.get('level')

    def get_player_info(self):
        player_info = ClashAPI().get_player_info_from_tag(self.player_tag)
        self.town_hall_level = player_info.get('townHallLevel')
        self.player_name = player_info.get('name')
        self.donations_given = player_info.get('donations')
        self.donations_received = player_info.get('donationsReceived')
        self.war_stars = player_info.get('warStars')
        self.attack_wins = player_info.get('attackWins')
        self.defense_wins = player_info.get('defenseWins')
        self.current_trophies = player_info.get('trophies')

        self.parse_hero_info(player_info.get('heroes'))



class ClanData:
    def __init__(self, tag):
        self.tag = tag
        self.clan_name = None
        self.clan_level = None
        self.clan_points = None
        self.invite_only = None
        self.war_wins = None
        self.war_losses = None
        self.war_ties = None
        self.members_dict = {}
        self.member_count = None

        self.populate_clan_info()

    def get_player_detail_dict(self, player_list):
        self.member_count = len(player_list)

        for member in player_list:
            player_tag = member.get('tag', None)
            self.members_dict[player_tag] = PlayerData(player_tag)

        # return self.memberDict

    def populate_clan_info(self):
        allClanData = ClashAPI().get_clan_info_from_tag(self.tag)

        self.clan_name = allClanData.get('name', None)
        self.clan_level = allClanData.get('clanLevel', None)
        self.clan_points = allClanData.get('clanPoints', None)
        self.invite_only = allClanData.get('isWarLogPublic', None)
        member_list = allClanData.get('memberList', None)

        self.member_count = len(member_list)

        if self.invite_only:
            self.war_wins = allClanData.get('warWins', None)
            self.war_losses = allClanData.get('warLosses', None)

        # self.get_player_detail_dict(partialMemberList)

    def get_townhall_counts(self, active_only=False):

        townHallDict = {}

        def add_th():
            if player.townHallLevel in townHallDict.keys():
                townHallDict[player.townHallLevel] += 1
            else:
                townHallDict[player.townHallLevel] = 1

        for player in self.members_dict.values():

            player.get_player_info()

            if active_only:
                if player.donationsReceived + player.donationsGiven > 0:
                    add_th()
            else:
                add_th()

        pprint(townHallDict)

    def get_avg_hero_level_by_th(self, heroName, isActive=False):

        levelByTHSum = {}
        levelByTHCounts = {}

        if not heroName:
            raise ValueError('Please Provide the Name of a Hero: King, Queen, Warden, Battlemachine')
        else:
            heroName = heroName.lower()

        def sum_hero_levels(heroLevel):

            if player.townHallLevel in levelByTHSum.keys():
                levelByTHSum[player.townHallLevel] += heroLevel
                levelByTHCounts[player.townHallLevel] += 1
            else:
                levelByTHSum[player.townHallLevel] = heroLevel
                levelByTHCounts[player.townHallLevel] = 1

        for player in self.members_dict.values():

            player.get_player_info()

            heroDict = {
                'king': player.kingLevel,
                'queen': player.queenLevel,
                'warden': player.wardenLevel,
                'battlemachine': player.battleMachineLevel
            }

            heroLevel = heroDict[heroName]

            if isActive:
                if player.donationsReceived + player.donationsGiven > 10:
                    if heroLevel:
                        sum_hero_levels(heroLevel)
            else:
                if heroLevel:
                    sum_hero_levels(heroLevel)

        avgHeroLevelbyTH = {k: v/levelByTHCounts[k] for k, v in levelByTHSum.items()}
        # pprint(levelByTHSum)
        return avgHeroLevelbyTH
        # 'TH Counts: ', levelByTHCounts)
        # print('Levels: ', avgHeroLevelbyTH)
