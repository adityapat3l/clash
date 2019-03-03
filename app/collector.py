from __future__ import print_function
from app.api import ClashAPI
from pprint import pprint


class PlayerData:
    def __init__(self, tag):
        # super().__init__()
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
        self.clanLevel = None
        self.clanPoints = None
        self.isWarLogPublic = None
        self.warWins = None
        self.warLosses = None
        self.warTies = None
        self.memberDict = {}
        self.numMembers = None

    def get_player_detail_list(self, player_list):
        self.numMembers = len(player_list)

        for member in player_list:
            player_tag = member.get('tag', None)
            self.memberDict[player_tag] = PlayerData(player_tag)

    def get_all_clan_info(self):
        allClanData = ClashAPI().get_clan_info_from_tag(self.tag)

        self.clanLevel = allClanData.get('clanLevel', None)
        self.clanPoints = allClanData.get('clanPoints', None)
        self.isWarLogPublic = allClanData.get('isWarLogPublic', None)
        partialMemberList = allClanData.get('memberList', None)

        if self.isWarLogPublic:
            pass  # TODO: clanWins, clanLosses

        self.get_player_detail_list(partialMemberList)

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
                if player.donationsReceived + player.donationsGiven > 10:
                    add_th()
            else:
                add_th()

        pprint(townHallDict)








