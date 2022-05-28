from apps.admin import admin
from apps.authentication import authentication
from apps.authentication.views import check_authentication
from flask import request, Response, session, url_for, redirect, render_template, flash, g
from datetime import timedelta, date, datetime
import config



@admin.route("/")
@check_authentication
def panel():

    # getting user from global object context
    if 'user' in g:
        user = g.user
    else :
        user = None

    send = {
        'user': user,
    }
    
    return render_template("admin.html", **send)

