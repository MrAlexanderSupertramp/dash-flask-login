from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from os import path


db = SQLAlchemy()
# migrate = Migrate(app, db)


def init_app(app):
    if not path.exists('mysite/' + 'database.db') :
        
        db.init_app(app)
        db.create_all(app=app)

