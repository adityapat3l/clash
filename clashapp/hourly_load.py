from clashapp.fact_builder import FactLoader, PlayerBuilder, ClanBuilder
from clashapp.models import db
import time

CLAN_LIST = ['#228VGUUU0', '#YUPCJJCR']


def initialize_clan(clan_tag):
    """
    Populates the data for the whole clan and its members
    No facts for members
    Good for Initialization
    """
    clan = ClanBuilder(clan_tag)
    clan.make_clan_current_entry()
    clan_members = clan.clan.members

    member_tags = [member.tag for member in clan_members]

    for tag in member_tags:
        populate_player_current(tag)


def populate_player_current(player_tag):
    """
    Populates current entry for player only
    Quick to compute
    Good for regular updates
    """

    player = PlayerBuilder(player_tag)
    player.make_player_current_entry()


def populate_clan_facts(clan_tag):
    """
    Populates the facts for the whole clan and its members
    Adds facts for members
    """
    clan = ClanBuilder(clan_tag)
    clan.make_clan_current_entry()

    clan_members = clan.clan.members

    member_tags = [member.tag for member in clan_members]

    for tag in member_tags:
        populate_player_facts(tag)


def populate_player_facts(player_tag, fact_type=None):
    """
    Populates fact entry for player
    Quick to compute
    Adds to the 4 fact tables
    """

    player = PlayerBuilder(player_tag)

    fact_builder = FactLoader(player_tag=player_tag, player=player)
    fact_builder.make_achv_fact()
    fact_builder.make_hero_fact()
    fact_builder.make_spell_fact()
    fact_builder.make_troop_fact()


if __name__ == '__main__':

    # for clan in CLAN_LIST:
    #     initialize_clan(clan)

    start = time.time()

    for clan in CLAN_LIST:
        populate_clan_facts(clan)

    db.session.commit()

    print('Finished in {} seconds'.format(time.time() - start))
