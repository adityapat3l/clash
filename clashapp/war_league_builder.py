import datetime
from .models.player import PlayerCurrent
from .models import db
from .apiwrapper.api import PlayerAPI, ClanAPI
from .apiwrapper.player import SearchPlayer
from .apiwrapper.war_league import WarLeague
from .models.war_league import CwlRounds, CwlAttacks, CwlClanCurrent, CwlPlayerCurrent
from .fact_builder import ClanBuilder
from .hourly_load import populate_player_facts
from sqlalchemy import text


class LeagueBuilder:

    def __init__(self, league_data):
        self._league_data = league_data
        self.league = WarLeague(self._league_data)

    @classmethod
    def create_from_clan_tag(cls, clan_tag):
        league_data = ClanAPI().get_current_league_war(clan_tag)
        return cls(league_data)

    def create_cwl_current_records(self):
        db.engine.execute("SET FOREIGN_KEY_CHECKS = 0;")
        for clan in self.league.clans:
            print("CLAN NAME: {}".format(clan.name))
            exists = CwlClanCurrent.query.filter(CwlClanCurrent.clan_tag == clan.tag).scalar() is not None

            if not exists:
                clan_entry = CwlClanCurrent(clan_tag=clan.tag,
                                            clan_name=clan.name,
                                            season=self.league.season,
                                            )
                db.session.add(clan_entry)

                for member in clan._cwl_members:
                    member_entry = CwlPlayerCurrent(player_tag=member.tag,
                                                    player_name=member.name,
                                                    season=self.league.season,
                                                    clan_tag=clan.tag,
                                                    town_hall=member.town_hall)

                    db.session.add(member_entry)
                    populate_player_facts(member.tag)


    def populate_battle(self, battle):
        clan = battle.clan
        opponent = battle.opponent

        def add_attack(attack, season):
            if attack.exists:
                cwl_attack = CwlAttacks(player_tag=attack.player.tag,
                                        battle_tag=battle.tag,
                                        season=season,
                                        town_hall=attack.player.town_hall,
                                        player_pos=attack.map_position,
                                        stars=attack.stars,
                                        destruction=attack.destruction,
                                        defender_tag=attack.defender_tag
                                        )

                db.session.add(cwl_attack)

        for attack in clan.attacks:
            add_attack(attack, season=self.league.season)
        for attack in opponent.attacks:
            add_attack(attack, season=self.league.season)



    def populate_rounds(self):
        db.engine.execute("SET FOREIGN_KEY_CHECKS = 0;")
        for league_round in self.league.rounds:
            print("----- ROUND {} -----".format(league_round.round_number))
            for battle in league_round.battles:

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
                opponent_attacks = opponent_round.total_attacks

                exists = CwlRounds.query.filter_by(clan_tag=clan_tag,
                                           opponent_clan_tag=opponent_clan_tag).scalar() is not None

                if not exists:
                    round_entry = CwlRounds(battle_tag=battle_tag,
                                            round_number=league_round.round_number,
                                            season=season,
                                            clan_tag=clan_tag,
                                            clan_stars=clan_stars,
                                            clan_attacks=clan_attacks,
                                            clan_destruction=clan_destruction,
                                            opponent_clan_tag=opponent_clan_tag,
                                            opponent_stars=opponent_stars,
                                            opponent_destruction=opponent_destruction,
                                            opponent_attacks=opponent_attacks)
                    db.session.add(round_entry)
                    self.populate_battle(battle)















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




