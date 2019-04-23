import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
import logging

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "db/clashdatabase.db"))


flaskapp = Flask(__name__)
flaskapp.config["SQLALCHEMY_DATABASE_URI"] = config.MYSQL_URL
flaskapp.config['SQLALCHEMY_ECHO'] = False
flaskapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(flaskapp)


def _commit_to_database():
    """A shared function to make a
       commit to the database and
       handle exceptions if encountered.
    """
    try:
        logging.info("Successfully Commited")
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        logging.warning("There was an Error", err)
        logging.info("Succesfully Rolled-back")
    finally:
        db.session.close()
        logging.info("Session Closed")