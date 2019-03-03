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

if clan_tag == 'foraiur':
    clan_tag = '#YUPCJJCR'
elif clan_tag == 'forever-young':
    clan_tag = '#CUQLRJOG'
elif clan_tag == 'mincers':
    clan_tag = '#9G2VRYUJ'
elif clan_tag == 'elchavo':
    clan_tag = '#2UPC98G'
elif clan_tag == 'angrytigers':
    clan_tag = '#YJQGP2VG'
elif clan_tag == 'hamham':
    clan_tag = '#GVJ9Q9J8'
clan = ClanData(clan_tag)

clan.get_all_clan_info()
clan.get_townhall_counts(active_only=True)
# pprint(PlayerData('#VVV8V9QC').get_player_info())