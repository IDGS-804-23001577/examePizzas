import os
from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY = "ClaveSecreta"
    SESSION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:twoface05@localhost:3306/pizzeria_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False