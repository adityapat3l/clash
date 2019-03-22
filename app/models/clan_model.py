from clashmanager import db
from app.compute import clan as clan_math
from datetime import datetime
from app.collector import ClanData, ClashAPI

class ClansStatsRecent(db.Model):

    clan_id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    clan_tag = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    clan_name = db.Column(db.String(20), nullable=False)
    clan_level = db.Column(db.Integer, nullable=False)
    clan_points = db.Column(db.Integer, nullable=False)

    member_count = db.Column(db.Integer, nullable=False)
    invite_only = db.Column(db.Boolean, nullable=False)

    war_wins = db.Column(db.Integer)
    # first_seen_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)


    @classmethod
    def create(cls, clan_tag):
        _clan = ClanData(clan_tag)
        clan_entry = ClansStatsRecent(clan_tag=_clan.tag,
                         clan_name=_clan.clan_name,
                         clan_level=_clan.clan_level,
                         clan_points=_clan.clan_points,
                         member_count=_clan.member_count,
                         invite_only=_clan.invite_only,
                         war_wins=_clan.war_wins
                         )

        db.session.add(clan_entry)
        db.session.commit()


