import os
import datetime

class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '57e19ea558d4967a552d03deece34a70'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI="sqlite:///database.db"
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    
    MAIL_SERVER = "mail.krioskcreata.com"  
    MAIL_PORT = 2525
    MAIL_USERNAME = "mailer@krioskcreata.com" 
    MAIL_PASSWORD = "Krioskcreata@18"
    MAIL_USE_TLS = True  
    MAIL_USE_SSL = False 
    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    # SESSION_PERMANENT = True
    # PERMANENT_SESSION_LIFETIME =  datetime.timedelta(seconds=5)
    # SESSION_TYPE = "sqlalchemy"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI="sqlite:///database.db"
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="sqlite:///database.db"
    SECRET_KEY = '57e19ea558d4967a552d03deece34a70'
    TIMEZONE = 'Europe/Oslo'
 