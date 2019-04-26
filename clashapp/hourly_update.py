import clashapp.feeder as feeder
import config
from clashapp import db
import logging
import os
import datetime
import sys
from . import _commit_to_database, timber_handler

cur_dir = os.getcwd()
today_date = datetime.datetime.utcnow()

log_dir = os.path.join(cur_dir, 'logs/{date:%Y}/{date:%m}/{date:%d}'.format(date=today_date))

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(level=logging.INFO,
                    filename=log_dir+'/hourly_update.log',
                    filemode='a',
                    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)
logger.addHandler(timber_handler)


def update():

    logger.info("Starting Hourly Update")
    db.engine.execute('truncate table player_stats_current')
    logger.info("Player Stats Truncated & Starting Repopulate")
    for clan_tag in config.STARTING_CLAN_TAG_LIST:
        feeder.populate_historic_clan_details(clan_tag)
        feeder.rebuild_current_player_details(clan_tag)

    _commit_to_database()
    logger.info("Sucessfully Finished Update")


if __name__ == '__main__':
    try:
        update()
    except Exception as e:
        raise
