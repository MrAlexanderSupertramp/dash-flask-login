import os
import datetime

class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = '57e19ea558d4967a552d03deece34a70'
    SQLALCHEMY_DATABASE_URI="sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    SESSION_TIMEOUT = 60*60*24*30   # 30 days : seconds*minutes*hours*days
    TOKEN_TIMEOUT = 60*30          # 30 minutes : seconds*minutes
    TIMEZONE = 'Asia/Kolkata'
    MAIL_SERVER = "mail.krioskcreata.com"  
    MAIL_PORT = 2525
    MAIL_USERNAME = "mailer@krioskcreata.com" 
    MAIL_PASSWORD = "Krioskcreata@18"
    MAIL_USE_TLS = True  
    MAIL_USE_SSL = False

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
 