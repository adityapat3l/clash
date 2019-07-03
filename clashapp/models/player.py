from . import db
from datetime import datetime
from sqlalchemy import PrimaryKeyConstraint


class PlayerCurrent(db.Model):

    player_tag = db.Column(db.String(72), unique=True, nullable=False, primary_key=True)
    player_name = db.Column(db.String(72), nullable=False)
    player_league = db.Column(db.String(72))
    player_trophies = db.Column(db.Integer, nullable=False)
    attack_wins = db.Column(db.Integer, nullable=False)
    defense_wins = db.Column(db.Integer, nullable=False)
    donations = db.Column(db.Integer, nullable=False)
    received = db.Column(db.Integer, nullable=False)
    war_stars = db.Column(db.Integer, nullable=False)
    town_hall = db.Column(db.Integer, nullable=False)

    clan_tag = db.Column(db.String(72), db.ForeignKey("clan_current.clan_tag"), index=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)

    has_expiry = db.Column(db.Boolean, default=False)
    expiry_time = db.Column(db.DateTime)

    @property
    def active_in_last_day(self):
        return


class FactTroop(db.Model):
    __table_args__ = (
        PrimaryKeyConstraint('player_tag', 'fact_time'),
        {},
    )

    player_tag = db.Column(db.String(72), db.ForeignKey("player_current.player_tag"), index=True)
    fact_time = db.Column(db.DateTime, nullable=False)

    barbarian = db.Column(db.SmallInteger)
    archer = db.Column(db.SmallInteger)
    goblin = db.Column(db.SmallInteger)
    giant = db.Column(db.SmallInteger)
    wall_breaker = db.Column(db.SmallInteger)
    balloon = db.Column(db.SmallInteger)
    wizard = db.Column(db.SmallInteger)
    healer = db.Column(db.SmallInteger)
    dragon = db.Column(db.SmallInteger)
    pekka = db.Column(db.SmallInteger)
    minion = db.Column(db.SmallInteger)
    hog_rider = db.Column(db.SmallInteger)
    valkyrie = db.Column(db.SmallInteger)
    golem = db.Column(db.SmallInteger)
    witch = db.Column(db.SmallInteger)
    lava_hound = db.Column(db.SmallInteger)
    bowler = db.Column(db.SmallInteger)
    baby_dragon = db.Column(db.SmallInteger)
    miner = db.Column(db.SmallInteger)
    wall_wrecker = db.Column(db.SmallInteger)
    battle_blimp = db.Column(db.SmallInteger)
    ice_golem = db.Column(db.SmallInteger)
    electro_dragon = db.Column(db.SmallInteger)

    # TODO: Add Builder Hall Stats


class FactSpell(db.Model):
    __table_args__ = (
        PrimaryKeyConstraint('player_tag', 'fact_time'),
        {},
    )

    player_tag = db.Column(db.String(72), db.ForeignKey("player_current.player_tag"), index=True)
    fact_time = db.Column(db.DateTime, nullable=False)

    lightning = db.Column(db.SmallInteger)
    healing = db.Column(db.SmallInteger)
    rage = db.Column(db.SmallInteger)
    jump = db.Column(db.SmallInteger)
    freeze = db.Column(db.SmallInteger)
    poison = db.Column(db.SmallInteger)
    earthquake = db.Column(db.SmallInteger)
    haste = db.Column(db.SmallInteger)
    clone = db.Column(db.SmallInteger)
    skeleton = db.Column(db.SmallInteger)
    bat = db.Column(db.SmallInteger)


class FactHero(db.Model):
    __table_args__ = (
        PrimaryKeyConstraint('player_tag', 'fact_time'),
        {},
    )

    player_tag = db.Column(db.String(72), db.ForeignKey("player_current.player_tag"), index=True)
    fact_time = db.Column(db.DateTime, nullable=False)

    barbarian_king = db.Column(db.SmallInteger)
    archer_queen = db.Column(db.SmallInteger)
    grand_warden = db.Column(db.SmallInteger)
    battle_machine = db.Column(db.SmallInteger)


class FactAchv(db.Model):
    __table_args__ = (
        PrimaryKeyConstraint('player_tag', 'fact_time'),
        {},
    )
    player_tag = db.Column(db.String(72), db.ForeignKey("player_current.player_tag"), index=True)
    fact_time = db.Column(db.DateTime, nullable=False)

    town_halls_destroyed = db.Column(db.Integer)  # Humiliator
    walls_destroyed = db.Column(db.Integer)  # 'Wall Buster'
    spells_donated = db.Column(db.Integer)  # 'Sharing is caring',
    troops_donated = db.Column(db.Integer)  # 'Friend in Need'
    clan_game_points = db.Column(db.Integer)  # 'Games Champion'
    obstacles_removed = db.Column(db.Integer)  # Nice and Tidy
    dark_looted = db.Column(db.Integer)  # 'Heroic Heist'
    elixer_looted = db.Column(db.Integer)  # 'Elixir Escapade'
    gold_looted = db.Column(db.Integer)  # 'Gold Grab'



