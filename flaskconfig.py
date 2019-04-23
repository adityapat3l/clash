import config

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = config.MYSQL_URL

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True