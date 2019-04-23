import clashapp.feeder as feeder
import config
from clashapp import db
import logging
import os
import datetime
from . import _commit_to_database

cur_dir = os.getcwd()
today_date = datetime.datetime.utcnow()

log_dir = os.path.join(cur_dir, 'logs/{date:%Y}/{date:%m}/{date:%d}'.format(date=today_date))

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(level=logging.INFO,
                    filename=log_dir+'/hourly_update.log',
                    filemode='a',
                    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.getLogger(__name__)


def update():

    logging.info("Starting Hourly Update")
    db.engine.execute('truncate table player_stats_current')
    logging.info("Player Stats Truncated & Starting Repopulate")
    for clan_tag in config.STARTING_CLAN_TAG_LIST:
        feeder.populate_historic_clan_details(clan_tag)
        feeder.rebuild_current_player_details(clan_tag)

    _commit_to_database()
    logging.info("Sucessfully Finished Update")


if __name__ == '__main__':
    update()
