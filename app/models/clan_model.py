from clashmanager import db
from app.compute import clan as clan_math
from datetime import datetime
from app.collector import ClanData, ClashAPI
from app.models.player_model import PlayerStatsCurrent
from sqlalchemy.ext.associationproxy import association_proxy

def _member_find_or_create(player_tag):
    member = PlayerStatsCurrent.query.filter_by(player_tag=player_tag).first()
    return member or PlayerStatsCurrent.create_from_player_tag(player_tag=player_tag)

class ClanStatsCurrent(db.Model):

    clan_id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    clan_tag = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    clan_name = db.Column(db.String(20), nullable=False)
    clan_level = db.Column(db.Integer, nullable=False)
    clan_points = db.Column(db.Integer, nullable=False)

    member_count = db.Column(db.Integer, nullable=False)
    invite_only = db.Column(db.Boolean, nullable=False)

    war_wins = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)

    clan_members = db.relationship('PlayerStatsCurrent', backref=db.backref('current_clan', lazy='dynamic'))

    members = association_proxy('clan_members', 'player_tag',
                                creator=_member_find_or_create,
                                )

    @classmethod
    def create_from_tag(cls, clan_tag):
        _clan = ClanData(clan_tag)
        clan_entry = ClanStatsCurrent(clan_tag=_clan.clan_tag,
                                      clan_name=_clan.clan_name,
                                      clan_level=_clan.clan_level,
                                      clan_points=_clan.clan_points,
                                      member_count=_clan.member_count,
                                      invite_only=_clan.invite_only,
                                      war_wins=_clan.war_wins
                                      )

        db.session.add(clan_entry)

        return clan_entry

    @property
    # TODO: Add method to add best member
    def best_overall_attacker(self):
        return

    @property
    def highest_donator(self):
        return

    @property
    def highest_war_stars_earner(self):
        return

    def get_member_count_by_town_hall(self):
        pass

    def members_with_hero_level(self, hero_name=None, hero_level=None):
        pass


class HistoricClanStats(db.Model):
    pass