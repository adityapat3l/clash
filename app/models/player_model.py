from clashmanager import db
from app.compute import clan as clan_math
from datetime import datetime
from app.collector import PlayerData


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

    clan_tag = db.Column(db.String(20), db.ForeignKey("clan_stats_current.clan_tag"))
    # clan = db.relationship('ClanStatsCurrent', backref=db.backref('members', lazy=True))

    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create_from_player_tag(cls, player_tag):
        _player = PlayerData(player_tag)

        # _clan_tag = _player.clan_tag
        #
        # if _clan_tag:
        #     clan = PlayerStatsCurrent.query.filter_by(clan_tag=_clan_tag).first()
        #     if not clan:
        #         clan = ClanStatsCurrent.create_from_tag(_clan_tag)
        # else:
        #     return TypeError("Sorry this player is Clanless")

        player_entry = PlayerStatsCurrent(
                                        player_tag=_player.player_tag,
                                        player_name=_player.player_name,
                                        exp_level=_player.exp_level,
                                        current_trophies=_player.current_trophies,
                                        attack_wins=_player.attack_wins,
                                        defense_wins=_player.defense_wins,
                                        donations_given=_player.donations_given,
                                        donations_received=_player.donations_received,
                                        war_stars=_player.war_stars,
                                        town_hall_level=_player.town_hall_level,
                                        king_level=_player.king_level,
                                        queen_level=_player.queen_level,
                                        warden_level=_player.warden_level,
                                        battle_machine_Level=_player.battle_machine_Level,
                                        clan_tag=_player.clan_tag
                                       )

        db.session.add(player_entry)

        return player_entry


class HistoricPlayerStats(db.Model):
    pass
