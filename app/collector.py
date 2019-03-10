from __future__ import print_function, division
from app.api import ClashAPI
from pprint import pprint


class PlayerData:
    def __init__(self, tag):
        self.tag = tag
        self.name = None
        self.townHallLevel = None
        self.attackWins = None
        self.defenseWins = None
        self.bestTrophies = None
        self.donationsGiven = None
        self.donationsReceived = None
        self.expLevel = None
        self.kingLevel = None
        self.queenLevel = None
        self.wardenLevel = None
        self.battleMachineLevel = None
        self.warStars = None
        # self.get_player_info()

    def parse_hero_info(self, heroList):

        for hero in heroList:
            if hero['name'] == 'Barbarian King':
                self.kingLevel = hero.get('level')
            elif hero['name'] == 'Battle Machine':
                self.battleMachineLevel = hero.get('level')
            elif hero['name'] == 'Archer Queen':
                self.queenLevel = hero.get('level')
            elif hero['name'] == 'Grand Warden':
                self.wardenLevel = hero.get('level')

    def get_player_info(self):
        player_info = ClashAPI().get_player_info_from_tag(self.tag)
        self.townHallLevel = player_info.get('townHallLevel')
        self.name = player_info.get('name')
        self.donationsGiven = player_info.get('donations')
        self.donationsReceived = player_info.get('donationsReceived')
        self.warStars = player_info.get('warStars')
        self.attackWins = player_info.get('attackWins')
        self.defenseWins = player_info.get('defenseWins')

        self.parse_hero_info(player_info.get('heroes'))

        # print(player_info)


class ClanData:
    def __init__(self, tag):
        self.tag = tag
        self.clanName = None
        self.clanLevel = None
        self.clanPoints = None
        self.isWarLogPublic = None
        self.warWins = None
        self.warLosses = None
        self.warTies = None
        self.memberDict = {}
        self.memberCount = None

    def get_player_detail_dict(self, player_list):
        self.memberCount = len(player_list)

        for member in player_list:
            player_tag = member.get('tag', None)
            self.memberDict[player_tag] = PlayerData(player_tag)

        # return self.memberDict

    def get_all_clan_info(self):
        allClanData = ClashAPI().get_clan_info_from_tag(self.tag)

        self.clanName = allClanData.get('name', None)
        self.clanLevel = allClanData.get('clanLevel', None)
        self.clanPoints = allClanData.get('clanPoints', None)
        self.isWarLogPublic = allClanData.get('isWarLogPublic', None)
        partialMemberList = allClanData.get('memberList', None)

        if self.isWarLogPublic:
            self.warWins = allClanData.get('warWins', None)
            self.warLosses = allClanData.get('warLosses', None)

        self.get_player_detail_dict(partialMemberList)

    def get_townhall_counts(self, active_only=False):

        townHallDict = {}

        def add_th():
            if player.townHallLevel in townHallDict.keys():
                townHallDict[player.townHallLevel] += 1
            else:
                townHallDict[player.townHallLevel] = 1

        for player in self.memberDict.values():

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

        for player in self.memberDict.values():

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
