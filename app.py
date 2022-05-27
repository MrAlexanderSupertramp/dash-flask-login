# from main import app
# from apps import create_app
import os
from flask import Flask
from datetime import timedelta
from flask_session import Session
from os import path
import database
from flask_mail import Mail

# apps import
from apps.admin import admin
from apps.authentication import authentication

from flask_migrate import Migrate
from database import db
from extensions import mail

# models import
from apps.authentication.models import User


# mail = Mail()

def flask_app():

    # create flask-app
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')


    # initialize database by giving it flask app
    migrate = Migrate(app, db)
    database.init_app(app)
    
    app.config['SESSION_TYPE'] = "sqlalchemy"
    app.config['SESSION_SQLALCHEMY_TABLE'] = "sessions"
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['SESSION_PERMANENT'] = True
    app.permanent_session_lifetime = timedelta(seconds=1500)

    # sess = Session()
    # sess.init_app(app)

    # App registrar
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(authentication, url_prefix='/authentication')

    # session registration
    Session(app)

    # # mail registration
    # mail = Mail(app)
    
    mail.init_app(app)

    return app


# Running main app
app = flask_app()


if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
    # app.run(host="0.0.0.0", port=5000, threaded=True)