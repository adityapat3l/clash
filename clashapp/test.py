from clashapp.models import db
from clashapp.fact_builder import PlayerBuilder
from clashapp.apiwrapper.api import LeagueAPI, ClanAPI
from pprint import pprint
from clashapp.apiwrapper.war_league import WarLeagueBattle, MemberAttack, WarLeague
import json
from clashapp.war_league_builder import LeagueBuilder
from clashapp.models.war_league import CwlPlayerCurrent, CwlClanCurrent, CwlAttacks, CwlRounds

# league = LeagueBuilder('#YUPCJJCR')
# print(league.populate_cwl_clan_current())



# if not:
# league_data = ClanAPI().get_current_league_war('#YUPCJJCR')

# if not league_data:
# league_data = json.load(open('clashapp/league_data.json'))

# with open('clashapp/league_data_mini.json', 'w') as f:
#     json.dump(league_data, f)


#
#
#
# league = WarLeague(league_data)
#
# print('____CLAN LEAGUE DATA FOR FOR AIUR____\n')
#
# print("KEYS: ", dir(league)[-5:])
#
# print("leagues.clans: ", league.clans)
#
# print("leagues.season: ", league.season)
#
# print("leagues.state: ", league.state)
#
# print("leagues.rounds: ", league.rounds)
#
# print("\n\n\n")
#
#
# print('_________ROUNDS___________\n')
#
# league_round = league.rounds[0]
#
# print("KEYS: ", dir(league_round)[-2:])
#
# print("league_round.round_number: ", league_round.round_number)
#
# print("league_round.battles: ", league_round.battles)
#
#
# print('_________BATTLES__________\n')
# battle = league_round.battles[0]
#
# print("KEYS: ", dir(battle)[-9:])
#
# print("battle.start_time: ", battle.start_time)
#
# print("battle.state: ", battle.state)
#
# print("battle.tag: ", battle.tag)
#
# print("battle.clan.stars: ", battle.clan.stars)
#
# print("battle.clan.destruction: ", battle.clan.destruction)
#
# print("battle.clan.total_attacks: ", battle.clan.total_attacks)
#
#
#
# print('_________CLAN_________\n')
# clan = battle.clan
#
# print("KEYS: ", dir(clan)[:])
# print("clan.stars: ", clan.stars)
# print("clan.destruction: ", clan.destruction)
#
# print("clan.attacks: ", clan.attacks)
#
#
#
# print('_________OPPONENT__________\n')
# opponent = battle.opponent
#
# print("KEYS: ", dir(opponent)[:])
# print("opponent.tag: ", opponent.tag)
# print("opponent.stars: ", opponent.stars)
# print("opponent.destruction: ", opponent.destruction)
# print("opponent.attacks: ", opponent.attacks)
#
#
#
# print('_________Attacks__________\n')
# member_attack = clan.attacks[1]
#
# print("KEYS: ", dir(member_attack)[:])
# print("member_attack.raw_map_position: ", member_attack.raw_map_position)
# print("member_attack.stars: ", member_attack.stars)
# print("member_attack.destruction: ", member_attack.destruction)
# print("member_attack.order: ", member_attack.order)
# print("member_attack.defender_tag: ", member_attack.defender_tag)
# print("member_attack.attacker_tag: ", member_attack.attacker_tag)
#
#


league = LeagueBuilder.from_clan_tag('#YUPCJJCR')
league.initialize_current_tables()
try:
    db.session.commit()
except Exception:
    db.session.rollback()
    raise
finally:
    db.session.close()
# CwlClanCurrent.__table__.create(db.session.bind, checkfirst=True)
# CwlPlayerCurrent.__table__.create(db.session.bind, checkfirst=True)


# CWL BATTLES

#['#290GCJGJY', '#290GCJQL2', '#290GCJJ0R', '#290GCJCPV', '#290C9RYGY', '#290C9RPP2', '#290C9RLUR',
# '#290C9RG8V', '#2920Q0282', '#2920Q09JR', '#2920LVVCC', '#2920LVUQQ', '#2929RURC9', '#2929RUC2Q',
#  '#2929RUQ8R', '#2929RUGLV', '#292LV8CQ9', '#292LV8PVC', '#292LV8GUR', '#292LV8J8V', '#292J8V8JY',
#  '#292J8VP0R', '#292J8UGUR', '#292J8UJ8V', '#292VLC0U2', '#292VLJPYC', '#292VLJYJ2', '#292VLJQ0Y']


