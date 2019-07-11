import datetime
from .models.player import PlayerCurrent
from .models import db
from .apiwrapper.api import PlayerAPI, ClanAPI
from .apiwrapper.player import SearchPlayer
from .apiwrapper.war_league import WarLeague
from .models.war_league import CwlRounds, CwlAttacks, CwlClanCurrent, CwlPlayerCurrent
from .fact_builder import ClanBuilder

class LeagueBuilder:

    def __init__(self, league_data):
        self._league_data = league_data
        self.league = WarLeague(self._league_data)

    @classmethod
    def from_clan_tag(cls, clan_tag):
        league_data = ClanAPI().get_current_league_war(clan_tag)
        return cls(league_data)

    def initialize_current_tables(self):
        for clan in self.league.clans:
            exists = CwlClanCurrent.query.filter(CwlClanCurrent.clan_tag == clan.tag).scalar() is not None

            if not exists:
                clan_entry = CwlClanCurrent(clan_tag=clan.tag,
                                            clan_name=clan.name,
                                            season=self.league.season,
                                       )
                db.session.add(clan_entry)
                db.session.commit()

                for member in clan._cwl_members:
                    member_entry = CwlPlayerCurrent(player_tag=member.tag,
                                                    player_name=member.name,
                                                    season=self.league.season,
                                                    clan_tag=clan.tag,
                                                    town_hall=member.town_hall)

                    db.session.add(member_entry)

    def populate_cwl_rounds(self):
        for league_rounds in self.league.rounds:
            print("----- ROUND {} -----".format(league_rounds.round_number))
            for battle in league_rounds.battles:
                clan_round = battle.clan
                opponent_round = battle.opponent

                battle_tag = battle.tag
                season = self.league.season

                clan_tag = clan_round.tag
                clan_stars = clan_round.stars
                clan_destruction = clan_round.destruction
                clan_attacks = clan_round.total_attacks

                opponent_clan_tag = opponent_round.tag
                opponent_stars = opponent_round.stars
                opponent_destruction = opponent_round.destruction
                opponent_clan = opponent_round.total_attacks

                def insert_player_attacks(clan_attacks_list, opponent_attacks_list):
                    for attack in clan_attacks_list:
                        if attack.exists:
                            print(attack.stars, attack.destruction, attack.attacker_tag,
                                  attack.defender_tag, attack.raw_map_position)


                print(battle_tag, season, clan_tag, clan_stars, round(clan_destruction,2), clan_attacks)
                insert_player_attacks(clan_round.attacks, opponent_round.attacks)

                # Update Clan Current
                # Update Player Current
                # Insert Player Attacks


                # battle_tag = db.Column(db.String(72), unique=True, nullable=False)
                # season = db.Column(db.String(72), nullable=False)
                # round_number = db.Column(db.Integer)
                #
                # clan_tag = db.Column(db.Integer, db.ForeignKey("cwl_clan_current.clan_tag"))
                # clan_stars = db.Column(db.Integer, default=0)
                # clan_destruction = db.Column(db.Integer, default=0)
                #
                # opponent_clan_tag = db.Column(db.Integer, db.ForeignKey("cwl_clan_current.clan_tag"))
                # opponent_stars = db.Column(db.Integer, default=0)
                # opponent_destruction = db.Column(db.Integer, default=0)
                #
                # created_time = db.Column(db.DateTime, default=datetime.utcnow)
                # updated_time = db.Column(db.DateTime, default=datetime.utcnow)















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
        ClanBuilder(self.player.clan.tag).make_clan_current_entry()
        self.exists_in_db = self.check_if_player_exists()

    def get_player_from_api(self):
        player_wrapper = PlayerAPI()
        player_data = player_wrapper.get_player(self.player_tag)
        self.player = SearchPlayer(player_data)

    def make_player_current_entry(self):

        if self.exists_in_db:
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




