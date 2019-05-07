import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
import logging
import timber

timber_handler = timber.TimberHandler(source_id=config.TIMBER_SOURCE_ID, api_key=config.TIMBER_API_KEY)
logger = logging.getLogger(__name__)
logger.addHandler(timber_handler)

flaskapp = Flask(__name__)
flaskapp.config["SQLALCHEMY_DATABASE_URI"] = config.MYSQL_URL
flaskapp.config['SQLALCHEMY_ECHO'] = False
flaskapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(flaskapp)

API_KEY = config.DEV_ADMIN_API_KEY


def _commit_to_database():
    """A shared function to make a
       commit to the database and
       handle exceptions if encountered.
    """
    try:
        logger.info("Successfully Commited")
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        logger.warning("There was an Error", err)
        logger.info("Succesfully Rolled-back")
    finally:
        db.session.close()
        logger.info("Session Closed")