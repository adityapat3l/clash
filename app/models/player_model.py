from clashmanager import db


class PlayerStatsRecent(db.Model):

    player_id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    player_tag = db.Column('tag', db.String(20), unique=True, nullable=False, primary_key=True)
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

    clan_tag = db.Column(db.String(20), db.ForeignKey("clans_stats_recent.clan_tag"))
    clan = db.relationship('ClansStatsRecent', backref=db.backref('members', lazy=True))


    def __repr__(self):
        return "<Title: {}>".format(self.title)
