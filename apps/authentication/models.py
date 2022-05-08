from enum import unique
from main.database import db
from flask_login import UserMixin
import datetime



class User(db.Model, UserMixin) :
    __tablename__ = 'user'

    # if the table is already created and requesting for the new table with same name then maintain following line
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300))
    email = db.Column(db.String(300), unique=True)
    password = db.Column(db.String(300))
    password_hashed = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(100))
    token_age = db.Column(db.DateTime, default=None)

    def __init__(self, username, email, password, password_hashed, is_verified, token, token_age):
        self.username = username
        self.email = email
        self.password = password
        self.password_hashed = password_hashed
        self.is_verified = is_verified
        self.token = token
        self.token_age = token_age


    def __repr__(self):
        # return f'<User {self.id}>'
        return '<User {}>'.format(self.id)
