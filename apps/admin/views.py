from apps.admin import admin
from apps.authentication import authentication
from apps.authentication.views import check_authentication
from flask import request, Response, session, url_for, redirect, render_template, flash, g



@admin.route("/")
@check_authentication
def panel():

    user = g.user

    send = {
        'user': g.user,
    }
    
    return render_template("admin.html", send=send)

