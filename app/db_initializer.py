import app.feeder as feeder
import config
from clashmanager import db

def initialize():
    db.drop_all()
    db.create_all()

    for clan_tag in config.STARTING_CLAN_TAG_LIST:
        feeder.populate_clan_details(clan_tag)
        feeder.populate_historic_clan_details(clan_tag)

    db.session.commit()


if __name__ == '__main__':
    initialize()