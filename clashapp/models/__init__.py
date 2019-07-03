import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import timber


logger = logging.getLogger(__name__)
DATABASE_URL = os.environ['MYSQL_DEV_URL']

flaskapp = Flask(__name__)
flaskapp.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
flaskapp.config['SQLALCHEMY_ECHO'] = False
flaskapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(flaskapp)
