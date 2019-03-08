import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "db/clashdatabase.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# db.drop_all()
# db.create_all()


class Clash(db.Model):
    clan_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    clan_tag = db.Column(db.String(20), nullable=True)
    clan_name = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


@app.route('/', methods=["GET", "POST"])
def home():
    clash = None
    if request.form:
        try:
            clash = Clash(clan_id=request.form.get("title"))
            db.session.add(clash)
            db.session.commit()
        except Exception as e:
            print("Failed to add clan tag")
            print(e)
    clash = Clash.query.all()
    return render_template("home.html", clans=clash)


@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        clash = Clash.query.filter_by(clan_id=oldtitle).first()
        clash.clan_id = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update clan tag")
        print(e)
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    clan_id = request.form.get("title")
    clash = Clash.query.filter_by(clan_id=clan_id).first()
    db.session.delete(clash)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    app.run(debug=True)