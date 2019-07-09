from clashapp.models import db
from clashapp.fact_builder import PlayerBuilder
from clashapp.apiwrapper.api import LeagueAPI, ClanAPI
from pprint import pprint
from clashapp.apiwrapper.war_league import WarLeagueRound, MemberAttack, WarLeague



league_data = ClanAPI().get_current_league_war('#YUPCJJCR')

print(league_data.keys(), league_data.values())

league_aiur = WarLeague(league_data)

# Clans
clans = league_aiur.clans
# print([i.name for i in clans])



# Rounds
rounds = league_aiur.rounds
# print(rounds)

# for i in data_keys:
#     print(i['name'], len(i['members']))

# print(data['season'])

# for clan in data['clans']:
#     print(clan[''])

war_data = LeagueAPI().get_league_war_details('#290GCJGJY')

# print(war_data.keys())

# print(war_data['opponent'].keys())
#
# print('Opponent',war_data['opponent'].keys())
#
# print(war_data['clan'].keys())
#
# print('Clan Member',war_data['clan']['members'][0].keys())
#
# print(war_data['clan']['members'][0])

# print(war_data)

# print()
# print(war_data.keys())

# war_keys = war_data['clan'].keys()

# print(len(war_data['clan']['members']))


# for member in war_data['clan']['members']:
#     pprint(member)