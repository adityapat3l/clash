from .player import PlayerCurrent
from . import db
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import func


def print_townhall_counts(th_dict):

    output_text = '\n'
    for th, count in th_dict.items():
        th_text = 'Town Hall {th}: {count} \n'.format(th=th, count=count)

        output_text += th_text

    print(output_text)


def _member_find_or_create( player_tag):
    member = PlayerCurrent.query.filter_by(player_tag=player_tag).first()
    return member or PlayerCurrent.create_from_player_tag(player_tag=player_tag)


class ClanCurrent(db.Model):

    clan_tag = db.Column(db.String(72), unique=True, nullable=False, primary_key=True)
    clan_name = db.Column(db.String(72), nullable=False)
    clan_level = db.Column(db.Integer, nullable=False)
    clan_points = db.Column(db.Integer, nullable=False)

    member_count = db.Column(db.Integer, nullable=False)
    clan_type = db.Column(db.String(72), nullable=False)
    war_wins = db.Column(db.Integer)
    war_losses = db.Column(db.Integer)

    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)

    has_expiry = db.Column(db.Boolean, default=False)
    expiry_time = db.Column(db.DateTime)

    clan_members = db.relationship('PlayerCurrent', backref=db.backref('current_clan', lazy=True))

    members = association_proxy('clan_members', 'player_tag',
                                creator=_member_find_or_create)

    @property
    def highest_war_stars_earner(self):
        return PlayerCurrent.query \
            .filter(PlayerCurrent.clan_tag == self.clan_tag) \
            .order_by(PlayerCurrent.war_stars.desc()) \
            .first()

    # TODO: Improve the __repr__ function for member count
    def get_member_count_by_town_hall(self):
        data = db.session.query(PlayerCurrent.town_hall_level,
                                func.count(PlayerCurrent.town_hall_level)) \
            .filter(PlayerCurrent.clan_tag == self.clan_tag) \
            .group_by(PlayerCurrent.town_hall_level) \
            .all()

        grouped_data = {k: v for k, v in data}
        print_townhall_counts(grouped_data)
        return grouped_data


