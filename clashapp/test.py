from clashapp.models import db
from clashapp.fact_builder import PlayerBuilder
from clashapp.apiwrapper.api import LeagueAPI, ClanAPI
from pprint import pprint
from clashapp.apiwrapper.war_league import WarLeagueBattle, MemberAttack, WarLeague

league_data = ClanAPI().get_current_league_war('#YUPCJJCR')
league = WarLeague(league_data)

rounds = league.rounds
# battles = [j.tag for j in i.battles for i in rounds]

battle_tags = []
for battle in rounds:
   for b2 in battle.battles:
       battle_tags.append(b2.tag)

print(battle_tags)
print(len(battle_tags))





# CWL BATTLES

#['#290GCJGJY', '#290GCJQL2', '#290GCJJ0R', '#290GCJCPV', '#290C9RYGY', '#290C9RPP2', '#290C9RLUR',
# '#290C9RG8V', '#2920Q0282', '#2920Q09JR', '#2920LVVCC', '#2920LVUQQ', '#2929RURC9', '#2929RUC2Q',
#  '#2929RUQ8R', '#2929RUGLV', '#292LV8CQ9', '#292LV8PVC', '#292LV8GUR', '#292LV8J8V', '#292J8V8JY',
#  '#292J8VP0R', '#292J8UGUR', '#292J8UJ8V', '#292VLC0U2', '#292VLJPYC', '#292VLJYJ2', '#292VLJQ0Y']
