from clashapp import db
from datetime import datetime
from clashapp.collector import PlayerData
from clashapp.models import clan_model
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import INTEGER


def get_or_create_clan(clan_tag):

    if clan_tag:
        clan = PlayerStatsCurrent.query.filter_by(clan_tag=clan_tag).first()
        if not clan:
            clan = clan_model.ClanStatsCurrent.create_from_tag(clan_tag)

        return clan

class PlayerStatsCurrent(db.Model):

    player_id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    player_tag = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    player_name = db.Column(db.String(80), nullable=False)
    exp_level = db.Column(db.Integer, nullable=False)
    current_league = db.Column(db.String(20))
    current_trophies = db.Column(db.Integer, nullable=False)
    attack_wins = db.Column(db.Integer, nullable=False)
    defense_wins = db.Column(db.Integer, nullable=False)
    donations_given = db.Column(db.Integer, nullable=False)
    donations_received = db.Column(db.Integer, nullable=False)
    war_stars = db.Column(db.Integer, nullable=False)
    town_hall_level = db.Column(db.Integer, nullable=False)
    king_level = db.Column(db.Integer)
    queen_level = db.Column(db.Integer)
    warden_level = db.Column(db.Integer)
    battle_machine_Level = db.Column(db.Integer)
    achv_th_destroyed = db.Column(db.Integer)
    achv_total_donations = db.Column(db.Integer)
    achv_gold_looted = db.Column(INTEGER(unsigned=True))
    achv_elixer_looted = db.Column(INTEGER(unsigned=True))
    achv_dark_looted = db.Column(INTEGER(unsigned=True))

    clan_tag = db.Column(db.String(20), db.ForeignKey("clan_stats_current.clan_tag"), index=True)
    # clan = db.relationship('ClanStatsCurrent', backref=db.backref('members', lazy=True))

    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create_from_player_tag(cls, player_tag, player_obj=None, skip_clan_create=False):
        if not player_obj:
            player_obj = PlayerData(player_tag)

        _clan_tag = player_obj.clan_tag

        if not skip_clan_create:
            get_or_create_clan(_clan_tag)

        player_entry = PlayerStatsCurrent(
                                        player_tag=player_obj.player_tag,
                                        player_name=player_obj.player_name,
                                        exp_level=player_obj.exp_level,
                                        current_league=player_obj.league_name,
                                        current_trophies=player_obj.current_trophies,
                                        attack_wins=player_obj.attack_wins,
                                        defense_wins=player_obj.defense_wins,
                                        donations_given=player_obj.donations_given,
                                        donations_received=player_obj.donations_received,
                                        war_stars=player_obj.war_stars,
                                        town_hall_level=player_obj.town_hall_level,
                                        king_level=player_obj.king_level,
                                        queen_level=player_obj.queen_level,
                                        warden_level=player_obj.warden_level,
                                        battle_machine_Level=player_obj.battle_machine_Level,
                                        clan_tag=player_obj.clan_tag,
                                        achv_total_donations=player_obj.achv_total_donations,
                                        achv_th_destroyed=player_obj.achv_th_destroyed,
                                        achv_gold_looted=player_obj.achv_gold_looted,
                                        achv_elixer_looted=player_obj.achv_elixer_looted,
                                        achv_dark_looted=player_obj.achv_dark_looted
                                       )

        db.session.add(player_entry)

        return player_entry


class PlayerStatsHistoric(db.Model):

    # player_id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    player_tag = db.Column(db.String(20), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        PrimaryKeyConstraint('player_tag', 'created_time'),
        {},
    )

    player_name = db.Column(db.String(80), nullable=False)
    exp_level = db.Column(db.Integer, nullable=False)
    current_league = db.Column(db.String(20))
    current_trophies = db.Column(db.Integer, nullable=False)
    attack_wins = db.Column(db.Integer, nullable=False)
    defense_wins = db.Column(db.Integer, nullable=False)
    donations_given = db.Column(db.Integer, nullable=False)
    donations_received = db.Column(db.Integer, nullable=False)
    war_stars = db.Column(db.Integer, nullable=False)
    town_hall_level = db.Column(db.Integer, nullable=False)
    king_level = db.Column(db.Integer)
    queen_level = db.Column(db.Integer)
    warden_level = db.Column(db.Integer)
    battle_machine_Level = db.Column(db.Integer)
    achv_th_destroyed = db.Column(db.Integer)
    achv_total_donations = db.Column(db.Integer)
    achv_gold_looted = db.Column(INTEGER(unsigned=True))
    achv_elixer_looted = db.Column(INTEGER(unsigned=True))
    achv_dark_looted = db.Column(INTEGER(unsigned=True))

    # player_id = db.Column(db.Integer, db.ForeignKey("player_stats_current.player_id"), index=True)

    clan_tag = db.Column(db.String(20), db.ForeignKey("clan_stats_current.clan_tag"), index=True)
    # clan = db.relationship('ClanStatsCurrent', backref=db.backref('members', lazy=True))

    updated_time = db.Column(db.DateTime, default=datetime.utcnow)


    @classmethod
    def create_from_player_tag(cls, player_tag, player_obj=None, skip_clan_create=False):
        if not player_obj:
            player_obj = PlayerData(player_tag)

        _clan_tag = player_obj.clan_tag

        if not skip_clan_create:
            get_or_create_clan(_clan_tag)

        player_entry = PlayerStatsHistoric(
            player_tag=player_obj.player_tag,
            created_time=datetime.utcnow(),
            player_name=player_obj.player_name,
            exp_level=player_obj.exp_level,
            current_league=player_obj.league_name,
            current_trophies=player_obj.current_trophies,
            attack_wins=player_obj.attack_wins,
            defense_wins=player_obj.defense_wins,
            donations_given=player_obj.donations_given,
            donations_received=player_obj.donations_received,
            war_stars=player_obj.war_stars,
            town_hall_level=player_obj.town_hall_level,
            king_level=player_obj.king_level,
            queen_level=player_obj.queen_level,
            warden_level=player_obj.warden_level,
            battle_machine_Level=player_obj.battle_machine_Level,
            clan_tag=player_obj.clan_tag,
            achv_total_donations=player_obj.achv_total_donations,
            achv_th_destroyed=player_obj.achv_th_destroyed,
            achv_gold_looted=player_obj.achv_gold_looted,
            achv_elixer_looted=player_obj.achv_elixer_looted,
            achv_dark_looted=player_obj.achv_dark_looted
        )

        db.session.add(player_entry)

        return player_entry
