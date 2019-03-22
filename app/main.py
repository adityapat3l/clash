from app.api import ClashAPI
from pprint import pprint
from app.collector import ClanData, PlayerData
import argparse


parser = argparse.ArgumentParser(description="Enter Clan Info!")
parser.add_argument("-c", "--clan", help="Enter the clan tag with the #")
parser.add_argument("-p", "--player", help="Enter the player tag with the $+#")
parser.add_argument("--hero", help="Enter the hero name")
parser.add_argument("--active_only", help="Int - Only consider active players?", type=bool, default=False)
args = parser.parse_args()

clanTag = args.clan.lower() if args.clan else None
playerTag = args.player if args.player else None
heroName = args.hero if args.hero else None
isActive = bool(int(args.active_only) if args.active_only else False)

if clanTag == 'foraiur':
    clanTag = '#YUPCJJCR'
elif clanTag == 'forever-young':
    clanTag = '#CUQLRJOG'
elif clanTag == 'mincers':
    clanTag = '#9G2VRYUJ'
elif clanTag == 'elchavo':
    clanTag = '#2UPC98G'
elif clanTag == 'angrytigers':
    clanTag = '#YJQGP2VG'
elif clanTag == 'hamham':
    clanTag = '#GVJ9Q9J8'
elif clanTag == 'lightinghero':
    clanTag = '#89RJ2U0J'
elif clanTag == 'shankscrew':
    clanTag = '#YPCRU92'
clan = ClanData(clanTag)


clan.populate_clan_info()
# clan.get_townhall_counts(active_only=True)
print(clan.get_avg_hero_level_by_th(heroName, isActive=isActive))
# pprint(PlayerData('#VVV8V9QC').get_player_info())