from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "mymusic.db"))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.secret_key = "flask rocks!"

db = SQLAlchemy(app)