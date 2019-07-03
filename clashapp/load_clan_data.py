import datetime
from .models import player as player_models
from .models import clan as clan_models
from .models import db
from .apiwrapper.api import PlayerAPI, ClanAPI
from .apiwrapper.player import SearchPlayer
from .apiwrapper.clan import SearchClan

PlayerCurrent = player_models.PlayerCurrent
ClanCurrent = clan_models.ClanCurrent

class ClanBuilder:
    def __init__(self, clan_tag, clan=None):
        self.clan_tag = clan_tag
        self.clan = clan

        if not self.clan:
            self.get_clan_from_api()

        self.exists_in_db = self.check_if_clan_exists()

    def get_clan_from_api(self):
        clan_wrapper = ClanAPI()
        clan_data = clan_wrapper.get_clan(self.clan_tag)
        self.clan = SearchClan(clan_data)

    def check_if_clan_exists(self):
        clan_current_entry = ClanCurrent.query.filter(ClanCurrent.clan_tag == self.clan_tag).first()
        return clan_current_entry is not None

    def create_clan_current_entry(self):

        if self.exists_in_db:
            print("Clan Already Exists")
            return

        clan_entry = ClanCurrent(clan_tag=self.clan.tag,
                                 clan_name=self.clan.name,
                                 clan_points=self.clan.points,
                                 clan_level=self.clan.level,
                                 member_count=self.clan.member_count,
                                 clan_type=self.clan.type,
                                 war_wins=self.clan.war_wins,
                                 war_losses=self.clan.war_losses)
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
        ClanBuilder(self.player.clan.tag).create_clan_current_entry()
        self.exists_in_db = self.check_if_player_exists()

    def get_player_from_api(self):
        player_wrapper = PlayerAPI()
        player_data = player_wrapper.get_player(self.player_tag)
        self.player = SearchPlayer(player_data)

    def create_player_current_entry(self):

        if self.exists_in_db:
            print("Player Already Exists")
            return
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
                                     clan_tag=self.player.clan.tag)

        db.session.add(player_entry)

    def add_expiry(self):
        # TODO: Add Expiry for Discord Bot
        pass


class FactLoader:

    def __init__(self, player_tag, player=None):
        self.fact_time = datetime.datetime.utcnow()
        self.player_tag = player_tag
        self.player = PlayerBuilder(self.player_tag)

        self.player.create_player_current_entry()


    def make(self):
        pass

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    # There's no data in redshift before 2010-09-01 so don't bother trying to backfill.
    parser.add_argument('--clan_tag', type=str, required=True)
    args = parser.parse_args()

    clan_tag = args.clan_tag

    # populate_clan_details(clan_tag)
    # print(clan_tag)




