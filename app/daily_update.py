import app.feeder as feeder
import config
from clashmanager import db

def initialize():

    for clan_tag in config.STARTING_CLAN_TAG_LIST:
        feeder.populate_historic_clan_details(clan_tag)

if __name__ == '__main__':
    initialize()