import datetime
from .models.player import PlayerCurrent, FactHero, FactSpell, FactTroop, FactAchv
from .models.clan import ClanCurrent
from .models import db
from .apiwrapper.api import PlayerAPI, ClanAPI
from .apiwrapper.player import SearchPlayer
from .apiwrapper.clan import SearchClan


class ClanBuilder:
    def __init__(self, clan_tag, clan=None):
        self.clan_tag = clan_tag
        self.clan = clan

        if not self.clan:
            self.get_clan_from_api()

        self.exists_in_db = None

    def get_clan_from_api(self):
        clan_wrapper = ClanAPI()
        clan_data = clan_wrapper.get_clan(self.clan_tag)
        self.clan = SearchClan(clan_data)

    def check_if_clan_exists(self):
        clan_current_entry = ClanCurrent.query.filter(ClanCurrent.clan_tag == self.clan_tag).first()
        return clan_current_entry is not None

    def make_clan_current_entry(self):
        self.exists_in_db = self.exists_in_db or self.check_if_clan_exists()

        if self.exists_in_db:
            return

        clan_entry = ClanCurrent(clan_tag=self.clan.tag,
                                 clan_name=self.clan.name,
                                 clan_points=self.clan.points,
                                 clan_level=self.clan.level,
                                 member_count=self.clan.member_count,
                                 clan_type=self.clan.type,
                                 war_wins=self.clan.war_wins,
                                 war_losses=self.clan.war_losses)
        print('Adding Clan: {}'.format(self.clan.name))
        db.session.add(clan_entry)

    def add_expiry(self):
        # TODO: Add Expiry for Discord Bot
        pass


class PlayerBuilder:
    def __init__(self, player_tag, player=None):
        self.player_tag = player_tag
        self.player = player

        if not self.player:
            self.get_player_from_api()

        self.validate()

    def check_if_player_exists(self):
        player_current_entry = PlayerCurrent.query.filter(PlayerCurrent.player_tag == self.player_tag).first()
        return player_current_entry is not None

    def validate(self):
        if self.player.clan:
            ClanBuilder(self.player.clan.tag).make_clan_current_entry()

        self.exists_in_db = self.check_if_player_exists()

    def get_player_from_api(self):
        player_wrapper = PlayerAPI()
        player_data = player_wrapper.get_player(self.player_tag)
        self.player = SearchPlayer(player_data)

    def make_player_current_entry(self):

        if self.exists_in_db:
            return

        try:
            player_clan_tag = self.player.clan.tag
        except AttributeError:
            # Player is no longer in clan
            player_clan_tag = None
        player_entry = PlayerCurrent(player_tag=self.player.tag,
                                     player_name=self.player.name,
                                     player_league=self.player.league_rank,
                                     player_trophies=self.player.trophies,
                                     attack_wins=self.player.attack_wins,
                                     defense_wins=self.player.defense_wins,
                                     donations=self.player.donations,
                                     received=self.player.received,
                                     war_stars=self.player.war_stars,
                                     town_hall=self.player.town_hall,
                                     clan_tag=player_clan_tag)

        db.session.add(player_entry)

    def add_expiry(self):
        # TODO: Add Expiry for Discord Bot
        pass


class FactLoader:

    def __init__(self, player_tag, player=None):
        self.fact_time = datetime.datetime.utcnow()
        self.player_tag = player_tag

        self.player = player or PlayerBuilder(player_tag)

        if not self.player.exists_in_db:
            self.player.make_player_current_entry()
            db.session.commit()

    def make_hero_fact(self):

        fact_data_dict = self.player.player._db_hero_load_dict()
        hero_entry = FactHero(player_tag=self.player_tag,
                              fact_time=self.fact_time,
                              **fact_data_dict)
        db.session.add(hero_entry)

    def make_spell_fact(self):

        fact_data_dict = self.player.player._db_spell_load_dict()
        spell_entry = FactSpell(player_tag=self.player_tag,
                                fact_time=self.fact_time,
                                **fact_data_dict)

        db.session.add(spell_entry)

    def make_troop_fact(self):

        fact_data_dict = self.player.player._db_troop_load_dict()
        troop_entry = FactTroop(player_tag=self.player_tag,
                                fact_time=self.fact_time,
                                **fact_data_dict)

        db.session.add(troop_entry)

    def make_achv_fact(self,):

        fact_data_dict = self.player.player._db_achievement_load_dict()
        achv_entry = FactAchv(player_tag=self.player_tag,
                              fact_time=self.fact_time,
                              **fact_data_dict)

        db.session.add(achv_entry)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    # There's no data in redshift before 2010-09-01 so don't bother trying to backfill.
    parser.add_argument('--clan_tag', type=str, required=True)
    args = parser.parse_args()

    clan_tag = args.clan_tag

    # populate_clan_details(clan_tag)
    # print(clan_tag)




