from clashmanager import db
from app.compute import clan as clan_math
from datetime import datetime
from app.collector import ClanData, ClashAPI
from app.models.player_model import PlayerStatsCurrent
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import func

def _member_find_or_create(player_tag):
    member = PlayerStatsCurrent.query.filter_by(player_tag=player_tag).first()
    return member or PlayerStatsCurrent.create_from_player_tag(player_tag=player_tag)


def print_townhall_counts(th_dict):

    output_text = '\n'
    for th, count in th_dict.items():
        th_text = 'Town Hall {th}: {count} \n'.format(th=th, count=count)

        output_text += th_text

    print(output_text)

class ClanStatsCurrent(db.Model):

    clan_id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    clan_tag = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    clan_name = db.Column(db.String(20), nullable=False)
    clan_level = db.Column(db.Integer, nullable=False)
    clan_points = db.Column(db.Integer, nullable=False)

    member_count = db.Column(db.Integer, nullable=False)
    invite_only = db.Column(db.Boolean, nullable=False)

    war_wins = db.Column(db.Integer)
    war_losses = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)

    clan_members = db.relationship('PlayerStatsCurrent', backref=db.backref('current_clan', lazy=True))

    members = association_proxy('clan_members', 'player_tag',
                                creator=_member_find_or_create,
                                )

    @classmethod
    def create_from_tag(cls, clan_tag, clan_obj=None):
        if not clan_obj:
            clan_obj = ClanData(clan_tag)
        clan_entry = ClanStatsCurrent(clan_tag=clan_obj.clan_tag,
                                      clan_name=clan_obj.clan_name,
                                      clan_level=clan_obj.clan_level,
                                      clan_points=clan_obj.clan_points,
                                      member_count=clan_obj.member_count,
                                      invite_only=clan_obj.invite_only,
                                      war_wins=clan_obj.war_wins,
                                      war_losses=clan_obj.war_losses
                                      )

        db.session.add(clan_entry)
        return clan_entry

    @property
    # TODO: Add method to add best member
    def best_overall_attacker(self):
        return PlayerStatsCurrent.query\
                                 .filter(PlayerStatsCurrent.clan_tag == self.clan_tag)\
                                 .order_by(PlayerStatsCurrent.attack_wins.desc())\
                                 .first()

    @property
    def highest_donator(self):
        return PlayerStatsCurrent.query \
                                .filter(PlayerStatsCurrent.clan_tag == self.clan_tag) \
                                .order_by(PlayerStatsCurrent.donations_given.desc()) \
                                .first()

    @property
    def highest_war_stars_earner(self):
        return PlayerStatsCurrent.query \
                                .filter(PlayerStatsCurrent.clan_tag == self.clan_tag) \
                                .order_by(PlayerStatsCurrent.war_stars.desc()) \
                                .first()

    # TODO: Improve the __repr__ function for member count
    def get_member_count_by_town_hall(self):
        data = db.session.query(PlayerStatsCurrent.town_hall_level,
                                func.count(PlayerStatsCurrent.town_hall_level)) \
                                .filter(PlayerStatsCurrent.clan_tag == self.clan_tag) \
                                .group_by(PlayerStatsCurrent.town_hall_level) \
                                .all()

        grouped_data = {k: v for k, v in data}
        print_townhall_counts(grouped_data)
        return grouped_data

    def get_avg_hero_level_by_th(self, hero_name=None, hero_level=None):

        if not hero_name or not hero_level:
            raise ValueError("Please specify hero_name and hero_level kwargs")

        hero_name = hero_name.lower()

        hero_mapper = {
            'king': PlayerStatsCurrent.king_level,
            'queen': PlayerStatsCurrent.queen_level
        }

        data =  db.session.query(PlayerStatsCurrent.town_hall_level,
                                func.avg(hero_mapper[hero_name])) \
                                .filter(PlayerStatsCurrent.clan_tag == self.clan_tag) \
                                .group_by(PlayerStatsCurrent.town_hall_level) \
                                .all()

        return data

# class HistoricClanStats(db.Model):
#     pass


# db.session.query(models.PlayerStatsCurrent.town_hall_level, func.count(models.PlayerStatsCurrent.town_hall_level)).group_by(models.PlayerStatsCurrent.town_hall_level).all()