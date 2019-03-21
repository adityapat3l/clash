import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from app.collector import ClanData
import config

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "db/clashdatabase.db"))


flaskapp = Flask(__name__)
flaskapp.config["SQLALCHEMY_DATABASE_URI"] = database_file
flaskapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(flaskapp)

# db.drop_all()
# db.create_all()


class ClansStatsRecent(db.Model):
    __tablename__ = 'clanstats'
    clanTag = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    clanName = db.Column(db.String(20), nullable=False)
    clanLevel = db.Column(db.Integer, nullable=False)
    clanPoints = db.Column(db.Integer, nullable=False)
    memberCount = db.Column(db.Integer, nullable=False)
    inviteType = db.Column(db.String(20))
    warWins = db.Column(db.Integer)


    def __repr__(self):
        return "<Title: {}>".format(self.title)


class PlayerStatsRecent(db.Model):
    __tablename__ = 'playerstats'
    playerTag = db.Column('tag', db.String(20), unique=True, nullable=False, primary_key=True)
    playerName = db.Column('name', db.String(80), nullable=False)
    playerExpLevel = db.Column('exp_level', db.Integer, nullable=False)
    playerLeague = db.Column(db.String(20))
    playerTrophies = db.Column(db.Integer, nullable=False)
    attackWins = db.Column(db.Integer, nullable=False)
    defenseWins = db.Column(db.Integer, nullable=False)
    donationsGiven = db.Column(db.Integer, nullable=False)
    donationsReceived = db.Column(db.Integer, nullable=False)
    warStars = db.Column(db.Integer, nullable=False)
    townHallLevel = db.Column(db.Integer, nullable=False)
    kingLevel = db.Column(db.Integer)
    queenLevel = db.Column(db.Integer)
    wardenLevel = db.Column(db.Integer)
    battleMachineLevel = db.Column(db.Integer)

    clanTag = db.Column(db.String(20), db.ForeignKey("clanstats.clanTag"))
    clanName = db.Column(db.String(20), nullable=False)

    warWins = db.Column(db.Integer, nullable=False)
    warWinStreak = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return "<Title: {}>".format(self.title)


@flaskapp.route('/', methods=["GET", "POST"])
def home(**kwargs):
    clan = None
    clanInst = {}
    if request.form:
        try:
            clan = ClansStatsRecent(clanTag=request.form.get("title"))
            clanInst = ClanData(clan.clanTag)
            clanInst.get_all_clan_info()
            clan.clanLevel = clanInst.clanLevel
            clan.clanName = clanInst.clanName
            clan.avgQueenLevel = str(clanInst.get_avg_hero_level_by_th('queen'))

            clan.clanPoints = clanInst.clanPoints
            clan.memberCount = clanInst.memberCount
            clan.warWins = clanInst.warWins
            clan.warLosses = clanInst.warLosses

            # clan.members = list(clanInst.memberDict.values())
            #
            # print([i.kingLevel for i in clan.members])
            #
            # print(clanInst.memberDict)
            #
            # c = ClanData(clan.clanTag)
            # c.get_all_clan_info()
            # print(c.clanLevel)
            #
            # a = c.get_avg_hero_level_by_th('queen')
            #
            # print(a)


            db.session.add(clan)
            db.session.commit()
        except Exception as e:
            print("Failed to add clan tag")
            print(e)
    clan = ClansStatsRecent.query.all()
    return render_template("home.html", clans=clan)


@flaskapp.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        clan = ClansStatsRecent.query.filter_by(clanTag=oldtitle).first()
        clan.clanTag = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update clan tag")
        print(e)
    return redirect("/")


@flaskapp.route("/delete", methods=["POST"])
def delete():
    clanTag = request.form.get("title")
    clan = ClansStatsRecent.query.filter_by(clanTag=clanTag).first()
    db.session.delete(clan)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    db.session.commit()
    db.drop_all()
    db.create_all()
    flaskapp.run(debug=True)