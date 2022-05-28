from re import L
from textwrap import wrap
from apps.authentication import authentication
from apps.admin import admin
from flask import request, Response, session, url_for, redirect, render_template, flash, g
from functools import wraps
from datetime import timedelta, date, datetime
from database import db
from flask_session import Session
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail
from extensions import mail
from random import randrange
import threading
import config

# model import
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash


# decorator : check authentication
def check_authentication(f) :
    @wraps(f)
    def wrap(*args, **kwargs) :

        # redirect if user is not logged in
        if not session.get('email') :
            return redirect(url_for('authentication.signin'))

        # get user
        user = User.query.filter_by(email=session['email']).first()

        if user.is_verified == False:
            flash("Email is not verified.", category="error")
            return redirect(url_for('authentication.activation_init'))

        # fixing user as global object into context : make user available down the pipeline via flask.g
        g.user = user

        # finally call f. f() now haves access to g.user
        return f(*args, **kwargs)

    return wrap



# task-worker : mail
def task_mail(msg) :

    try :
        # send email
        mail.send(msg)

        # print the current thread
        # print(threading.current_thread().name)
    except :
        flash("Its not you, its us. Our mail-servers are facing issues.", category="error")
        return redirect(url_for('authentication.activation_init'))




# sign up
@authentication.route("/sign-up/", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        # data = request.form 
        username = request.form.get('username', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        password_repeat = request.form.get('password-repeat', None)

        # check if both the passwords are same
        if password != password_repeat :
            flash("Password doesn't match.", category="error")
            return redirect(url_for('authentication.signup'))
        
        # check if email is already used
        users_with_same_email = User.query.filter_by(email=email).count()
        if users_with_same_email > 0 :
            flash("Email already exists.", category="error")
            return redirect(url_for('authentication.signup'))

        # generate token
        token = randrange(100000, 999999)

        # adding user to the database (for now)
        new_user = User(username=username, email=email, password=password, password_hashed=generate_password_hash(password, method='sha256'), is_verified=False, token=token, token_age=datetime.today())
        db.session.add(new_user)
        db.session.commit()

        # send token 
        msg = Message('One Time Passcode from Dash for email-confirmation', sender=("Dash Activation", "mailer@krioskcreata.com"), recipients=[email])
        msg.html = "Helloow there. <br/><br/><br/> The one-time code generated for activation is <b>{}</b>. <br/><br/><br/><br/><br/> Have a great day ahead.".format(token)
        
        # task_mail_result = task_mail(msg)

        threading.Thread(target=task_mail(msg)).start()


        flash("Account Created. Please check the inbox for varification.", category="success")
        return redirect(url_for('authentication.activation_end', email=email))

    return render_template("authentication/sign_up.html")




# activation
@authentication.route("/activation-init/", methods=["GET", "POST"])
def activation_init():

    if request.method == 'POST' :

        email = request.form.get('email', None)
        user = User.query.filter_by(email=email).first()

        # filter for advance query
        # user = User.query.filter(User.email==email).first()

        if not user :
            flash("Email does not exist.", category="error")
            return redirect(url_for('authentication.signup'))

        if user.is_verified == True :
            flash("Email is already varified.", category="error")
            return redirect(url_for('authentication.signin'))

        # generate token
        token = randrange(100000, 999999)

        user.token = token
        user.is_verified = False
        user.token_age = datetime.today()
        db.session.commit()

        # send token 
        msg = Message('One Time Passcode from Dash for email-confirmation', sender=("Dash Activation", "mailer@krioskcreata.com"), recipients=[email])
        msg.html = "Helloow there. <br/><br/><br/> The one-time code generated for activation is <b>{}</b>. <br/><br/><br/><br/><br/> Have a great day ahead.".format(token)
        
        threading.Thread(target=task_mail(msg)).start()


        flash("Email has been dispached.", category="success")
        return redirect(url_for('authentication.activation_end', email=email))

    # print(datetime.today())

    return render_template("authentication/activation_init.html")


@authentication.route("/activation-end", methods=["GET", "POST"])
def activation_end():

    if request.method == 'POST' :

        email = request.form.get('email', None)
        token = request.form.get('token', None)
        user = User.query.filter_by(email=email).first()

        if not user :
            flash("Email does not exist.", category="error")
            return redirect(url_for('authentication.signup'))

        if user.is_verified == True :
            flash("Email is already varified.", category="error")
            return redirect(url_for('authentication.signin'))

        if user.token :
            if user.token == token :

                try :
                    if ((datetime.today() - user.token_age) > timedelta(seconds=config.Config.TOKEN_TIMEOUT)) == True :
                        flash("The token has been expired.", category="error")
                        return redirect(url_for('authentication.forgot_password_init'))

                except :
                    flash("Its not you, its us. Please try again.", category="error")
                    return redirect(url_for('authentication.forgot_password_init'))

                user.is_verified = True
                db.session.commit()

                # set session
                session["email"] = email

                flash("The email has been verified.", category="success")
                return redirect(url_for('admin.panel'))

            else :
                flash("Incorrect token.", category="error")
                return redirect(url_for('authentication.activation_end', email=email))
        else :
            flash("Its not you, its us. Please try again.", category="error")
            return redirect(url_for('authentication.activation_init'))


    email = request.args.get('email', default=None, type=None)
    user = User.query.filter_by(email=email).first()

    if not user :
        flash("Email does not exist.", category="error")
        return redirect(url_for('authentication.signup'))

    if user.is_verified == True :
        flash("Email is already varified.", category="error")
        return redirect(url_for('authentication.signin'))

    send = {
        'email': email,
    }

    return render_template("authentication/activation_end.html", **send)




# sign in
@authentication.route("/sign-in", methods=["GET", "POST"])
def signin():
    if request.method == 'POST':

        email = request.form.get('email', None)
        password = request.form.get('password', None)

        user = User.query.filter_by(email=email).first()
        # user = User.query.filter(User.email==email).all()

        if not user :
            flash("Email does not exist. Please Sign-Up.", category="error")
            return redirect(url_for('authentication.signin'))

        if password != user.password :
            flash("Incorrect password.", category="error")
            return redirect(url_for('authentication.signin'))

        if user.is_verified != True :
            flash("Email is not verified. Please verify the email.", category="error")
            return redirect(url_for('authentication.activation_init'))

        session["email"] = email
        # session["password"] = password
        return redirect(url_for('admin.panel'))

    return render_template("authentication/sign_in.html")




# forgot password
@authentication.route("/forgot-password-init", methods=["GET", "POST"])
def forgot_password_init():

    if request.method == 'POST' :

        email = request.form.get('email', None)
        user = User.query.filter_by(email=email).first()

        if not user :
            flash("Email does not exist.", category="error")
            return redirect(url_for('authentication.signup'))

        if user.is_verified != True :
            flash("Email is not verified.", category="error")
            return redirect(url_for('authentication.activation_init'))

        # generate token
        token = randrange(100000, 999999)

        user.token = token
        user.token_age = datetime.today()
        db.session.commit()

        # send token
        msg = Message('One Time Passcode from Dash for password-reset', sender=("Dash Password-Reset", "mailer@krioskcreata.com"), recipients=[email])
        msg.html = "Helloow there. <br/><br/><br/> The one-time code generated for password-reset is <b>{}</b>. <br/><br/><br/><br/><br/> Have a great day ahead.".format(token)
        
        threading.Thread(target=task_mail(msg)).start()


        flash("Email has been dispached for Password-Reset.", category="success")
        return redirect(url_for('authentication.forgot_password_end', email=email))

    return render_template("authentication/forgot_password_init.html")


@authentication.route("/forgot-password-end", methods=["GET", "POST"])
def forgot_password_end():

    if request.method == 'POST' :

        email = request.form.get('email', None)
        token = request.form.get('token', None)
        password = request.form.get('password', None)
        password_repeat = request.form.get('password-repeat', None)

        user = User.query.filter_by(email=email).first()

        if not user :
            flash("Email does not exist.", category="error")
            return redirect(url_for('authentication.signup'))

        if user.is_verified != True :
            flash("Email is not verified.", category="error")
            return redirect(url_for('authentication.activation_init'))

        # check if both the passwords are same
        if password != password_repeat :
            flash("Password doesn't match.", category="error")
            return redirect(url_for('authentication.signup'))
        
        if user.token :
            if user.token == token :

                try :

                    if ((datetime.today() - user.token_age) > timedelta(seconds=config.Config.TOKEN_TIMEOUT)) == True :
                        flash("The token has been expired.", category="error")
                        return redirect(url_for('authentication.forgot_password_init'))

                except :
                    flash("Its not you, its us. Please try again.", category="error")
                    return redirect(url_for('authentication.forgot_password_init'))


                user.password = password
                db.session.commit()

                # set session
                session["email"] = email

                flash("The password has been changed.", category="success")
                return redirect(url_for('admin.panel'))

            else :
                flash("Incorrect token.", category="error")
                return redirect(url_for('authentication.activation_end', email=email))
        else :
            flash("Its not you, its us. Please try again.", category="error")
            return redirect(url_for('authentication.forgot_password_init'))

    
    email = request.args.get('email', default=None, type=None)

    send = {
        'email': email,
    }

    return render_template("authentication/forgot_password_end.html", **send)




# sign out
@authentication.route("/logout")
def signout():

    try :
        session.pop('email', None)

        flash("Logged out Successfully.", category="success")
    except :
        pass

    return redirect(url_for('authentication.signin'))




# test-mail
@authentication.route("/test-mail", methods=["GET", "POST"])
def test_mail() :

    email = request.args.get('email', default=None, type=None)

    # msg structure : text, sender, 
    msg = Message('Test mail', sender=("Dash-Test", "mailer@krioskcreata.com"), recipients=[email])
    msg.html = "This is for test purpose"
    mail.send(msg)

    return Response("Test-Mail has been dispached to " + email)
