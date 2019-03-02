from __future__ import print_function
from app.api import ClashAPI
from pprint import pprint
# pprint(ClashAPI().get_player_info_from_tag('#8292J8QV8'))

# clan_data = pprint(ClashAPI().get_clan_info_from_tag('#YUPCJJCR'))


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
            self.kingLevel = hero.get('level') if hero['name'] == 'Barbarian King' else None
            self.battleMachineLevel = hero.get('level') if hero['name'] == 'Battle Machine' else None
            self.queenLevel = hero.get('level') if hero['name'] == 'Archer Queen' else None
            self.wardenLevel = hero.get('level') if hero['name'] == 'Grand Warden' else None

    def get_player_info(self):
        player_info = ClashAPI().get_player_info_from_tag(self.tag)
        self.townHallLevel = player_info.get('townHallLevel')
        self.name = player_info.get('name')
        # self.kingLevel = player_info.get('heroes').get('level')
        self.parse_hero_info(player_info.get('heroes'))

        # print(self.name, self.townHallLevel)

        return player_info

        # print(player_info.keys())






class ClanData:
    def __init__(self, tag):
        # super().__init__()
        self.tag = tag
        self.clanLevel = None
        self.clanPoints = None
        self.isWarLogPublic = None
        self.warWins = None
        self.warLosses = None
        self.warTies = None
        self.memberList = []
        self.numMembers = None

    def get_player_detail_list(self, player_list):
        self.numMembers = len(player_list)

        player_dict = {}
        for member in player_list:
            player_tag = member.get('tag', None)
            player_dict['tag'] = player_tag
            # print(player_tag)

            player_inst = PlayerData(player_tag)
            player_dict['object'] = player_inst
            self.memberList.append(player_inst.get_player_info())  # TODO: FIX THIS SHIT - SAVE INSTANCES NOT DICT

            # print(self.memberList)
            # print("\n\n\n")


    def get_all_clan_info(self):
        allClanData = ClashAPI().get_clan_info_from_tag(self.tag)

        self.clanLevel = allClanData.get('clanLevel', None)
        self.clanPoints = allClanData.get('clanPoints', None)
        self.isWarLogPublic = allClanData.get('isWarLogPublic', None)
        partialMemberList = allClanData.get('memberList', None)

        if self.isWarLogPublic:
            pass  # TODO: clanWins, clanLosses

        self.get_player_detail_list(partialMemberList)

        # print(self.memberList)

    def get_townhall_counts(self):

        townHallDict = {}

        for player_dict in self.memberList:

            if player_dict['townHallLevel'] in townHallDict.keys():
                townHallDict[player_dict['townHallLevel']] += 1
            else:
                townHallDict[player_dict['townHallLevel']] = 1

        pprint(townHallDict)








