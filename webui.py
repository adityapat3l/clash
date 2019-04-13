from clashapp import flaskapp, db
from clashapp.models import clan_model, player_model
from flask import render_template, request, redirect
from clashapp.collector import ClanData


@flaskapp.route('/', methods=["GET", "POST"])
def home(**kwargs):
    clan = None
    clanInst = {}
    if request.form:
        try:
            clan = clan_model.ClansStatsRecent(clanTag=request.form.get("title"))
            clanInst = ClanData(clan.clan_tag)
            clanInst.populate_clan_info()
            clan.clanLevel = clanInst.clan_level
            clan.clanName = clanInst.clan_name
            clan.avgQueenLevel = str(clanInst.get_avg_hero_level_by_th('queen'))

            clan.clanPoints = clanInst.clan_points
            clan.memberCount = clanInst.member_count
            clan.warWins = clanInst.war_wins
            clan.warLosses = clanInst.war_losses

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
    clan = clan_model.ClansStatsRecent.query.all()
    return render_template("home.html", clans=clan)


@flaskapp.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        clan = clan_model.ClansStatsRecent.query.filter_by(clanTag=oldtitle).first()
        clan.clanTag = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update clan tag")
        print(e)
    return redirect("/")


@flaskapp.route("/delete", methods=["POST"])
def delete():
    clanTag = request.form.get("title")
    clan = clan_model.ClansStatsRecent.query.filter_by(clanTag=clanTag).first()
    db.session.delete(clan)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    flaskapp.run(debug=True)