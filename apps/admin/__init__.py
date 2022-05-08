from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy


# creating blueprint
admin = Blueprint('admin', __name__)
# admin = Blueprint('admin', __name__, template_folder="templates", static_folder="static")


# importing all the routes/functions from blog-app. Can import individual routes/functions too.
from . import views

