from flask import Blueprint



# creating blueprint
authentication = Blueprint('authentication', __name__)

from . import views


