from . import db
from datetime import datetime
from sqlalchemy import PrimaryKeyConstraint


class CwlClanCurrent(db.Model):

    __table_args__ = (
        PrimaryKeyConstraint('clan_tag', 'season'),
        {},
    )

    clan_tag = db.Column(db.String(72), unique=True, nullable=False)
    clan_name = db.Column(db.String(72), nullable=False)
    season = db.Column(db.String(72), nullable=False)

    stars_for = db.Column(db.Integer, default=0)
    destruction_for = db.Column(db.Integer, default=0)
    attacks_for = db.Column(db.Integer, default=0)

    stars_against = db.Column(db.Integer, default=0)
    destruction_against = db.Column(db.Integer, default=0)
    attacks_against = db.Column(db.Integer, default=0)

    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)


class CwlPlayerCurrent(db.Model):
    __table_args__ = (
        PrimaryKeyConstraint('player_tag', 'season'),
        {},
    )

    player_tag = db.Column(db.String(72), unique=True, nullable=False)
    player_name = db.Column(db.String(72), nullable=False)
    season = db.Column(db.String(72), nullable=False)
    clan_tag = db.Column(db.String(72), db.ForeignKey("cwl_clan_current.clan_tag"), nullable=True)
    town_hall = db.Column(db.Integer)

    battles_fought = db.Column(db.Integer, default=0)

    stars_for = db.Column(db.Integer, default=0)
    destruction_for = db.Column(db.Integer, default=0)
    attacks_for = db.Column(db.Integer, default=0)

    stars_against = db.Column(db.Integer, default=0)
    destruction_against = db.Column(db.Integer, default=0)
    attacks_against = db.Column(db.Integer, default=0)

    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)


class CwlAttacks(db.Model):

    __table_args__ = (
        PrimaryKeyConstraint('battle_tag', 'player_tag'),
        {},
    )

    player_tag = db.Column(db.String(72), nullable=False)
    battle_tag = db.Column(db.String(72), nullable=False)
    season = db.Column(db.String(72), nullable=False)
    town_hall = db.Column(db.Integer)

    player_pos = db.Column(db.String(72), nullable=False)
    stars = db.Column(db.Integer, default=0)
    destruction = db.Column(db.Integer, default=0)

    defender_tag = db.Column(db.String(72))
    defender_pos = db.Column(db.Integer)
    defender_town_hall = db.Column(db.Integer)

    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)


class CwlRounds(db.Model):

    __table_args__ = (
        PrimaryKeyConstraint('battle_tag', 'clan_tag'),
        {},
    )

    battle_tag = db.Column(db.String(72), unique=True, nullable=False)
    season = db.Column(db.String(72), nullable=False)
    round_number = db.Column(db.Integer)

    clan_tag = db.Column(db.String(72), db.ForeignKey("cwl_clan_current.clan_tag"))
    clan_stars = db.Column(db.Integer, default=0)
    clan_destruction = db.Column(db.Integer, default=0)
    clan_attacks = db.Column(db.Integer, default=0)

    opponent_clan_tag = db.Column(db.String(72), db.ForeignKey("cwl_clan_current.clan_tag"))
    opponent_stars = db.Column(db.Integer, default=0)
    opponent_destruction = db.Column(db.Integer, default=0)
    opponent_attacks = db.Column(db.Integer, default=0)

    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)
