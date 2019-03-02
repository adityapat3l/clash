from app.api import ClashAPI
from pprint import pprint
from app.collector import ClanData, PlayerData
import argparse


parser = argparse.ArgumentParser(description="Enter Clan Info!")
parser.add_argument("-c", "--clan", help="Your nobel profession")
parser.add_argument("-p", "--player", help="Your nobel profession")
args = parser.parse_args()

clan_tag = args.clan.lower() if args.clan else None
player_tag = args.player if args.player else None

if clan_tag == 'fy':
    clan_tag = '#YUPCJJCR'
elif clan_tag == 'en':
    clan_tag = '#CUQLRJOG'


clan = ClanData(clan_tag)

clan.get_all_clan_info()
clan.get_townhall_counts()
# pprint(PlayerData().get_player_info('#VVV8V9QC'))