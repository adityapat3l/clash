import clashapp.feeder as feeder
import config
from clashapp import db
from clashapp.models import ClanStatsCurrent

def update():

    db.engine.execute('truncate table player_stats_current')
    for clan_tag in config.STARTING_CLAN_TAG_LIST:
        feeder.populate_historic_clan_details(clan_tag)
        feeder.rebuild_current_player_details(clan_tag)


if __name__ == '__main__':
    update()
