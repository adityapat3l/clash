from clashapp.models import PlayerStatsCurrent, ClanStatsCurrent, PlayerStatsHistoric
from clashapp.collector import ClanData, PlayerData
from sqlalchemy import exists
from clashapp import db
from . import _commit_to_database, timber_handler
import logging
import traceback
import sys

logger = logging.getLogger(__name__)
logger.addHandler(timber_handler)

# TODO: Make this a class so that ClanData and PlayerData only get called once when functions are used multiple times.

def populate_member_details(player_tag):
    player = PlayerData(player_tag)
    PlayerStatsCurrent.create_from_player_tag(player_tag, player_obj=player, skip_clan_create=True)


def populate_historic_member_details(player_tag):
    player = PlayerData(player_tag)
    PlayerStatsHistoric.create_from_player_tag(player_tag, player_obj=player, skip_clan_create=True)


def populate_clan_details_init(clan_tag):

    existing_clan = ClanStatsCurrent.query.filter_by(clan_tag=clan_tag).first()
    if existing_clan:
        name = existing_clan.clan_name
        print("Sorry, clan '{name}' has already been created".format(name=name))
        return existing_clan

    clan = ClanData(clan_tag)
    ClanStatsCurrent.create_from_tag(clan_tag, clan_obj=clan)
    members_list = clan.member_list_raw

    for member in members_list:
        member_tag = member.get('tag')
        populate_member_details(member_tag)

    _commit_to_database()


def populate_historic_clan_details(clan_tag):

    logger.info("Populating Player Stats History For Clan: {}".format(clan_tag))
    try:
        clan = ClanData(clan_tag)
        members_list = clan.member_list_raw

        for member in members_list:
            member_tag = member.get('tag')
            populate_historic_member_details(member_tag)
    except Exception as err:
        logger.error("Player Stats History Populate Failed")
        logger.error(err.args)
        logger.error(traceback.format_exception(*sys.exc_info()))


def rebuild_current_player_details(clan_tag):

    logger.info("Re-populating Player Current For Clan: {}".format(clan_tag))

    try:
        clan = ClanData(clan_tag)
        members_list = clan.member_list_raw

        for member in members_list:
            member_tag = member.get('tag')
            populate_member_details(member_tag)
    except Exception as err:
        logger.error("Re-Populate Failed")
        logger.error(err.args)
        logger.error(traceback.format_exception(*sys.exc_info()))