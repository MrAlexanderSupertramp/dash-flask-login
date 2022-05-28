import os
import datetime

class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = '57e19ea558d4967a552d03deece34a7000'
    SQLALCHEMY_DATABASE_URI="sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    SESSION_TIMEOUT = 60*60*24*30   # 30 days : seconds*minutes*hours*days
    TOKEN_TIMEOUT = 60*30          # 30 minutes : seconds*minutes
    TIMEZONE = 'Asia/Kolkata'
    MAIL_SERVER = ""     #string
    MAIL_PORT = 2525     #integer
    MAIL_USERNAME = ""   #string
    MAIL_PASSWORD = ""   #string
    MAIL_USE_TLS = False #boolean
    MAIL_USE_SSL = False #boolean

    # TESTING = False
    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # SESSION_PERMANENT = True
    # PERMANENT_SESSION_LIFETIME =  datetime.timedelta(seconds=5)
    # SESSION_TYPE = "sqlalchemy"

class ProductionConfig(Config):
    ENV="production"
    DEBUG = False
 

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True
 