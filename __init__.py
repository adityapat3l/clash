# import os
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import config
#
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_file = "sqlite:///{}".format(os.path.join(project_dir, "db/clashdatabase.db"))
#
#
# flaskapp = Flask(__name__)
# flaskapp.config["SQLALCHEMY_DATABASE_URI"] = config.MYSQL_URL
# flaskapp.config['SQLALCHEMY_ECHO'] = False
# flaskapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(flaskapp)

# if __name__ == '__main__':
#     import clashapp.models
#     db.create_all()
