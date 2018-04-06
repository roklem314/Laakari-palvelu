from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
import bcrypt
import time

from application import app
from application.registration.models import Users
from application.appointment.models import Appointment
from application.auth.forms import LoginForm

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()


    if form.validate_on_submit():

        user = Users.query.filter_by(email=form.email.data).first()
        # if user is None or not user.check_password(form.password.data):
        time.sleep(10)
        if user is None or not bcrypt.checkpw(form.password.data.encode("utf-8"), user.password):
            time.sleep(10)
            return render_template("auth/login.html", form = form, error = "Salasana tai email eivät täsmää!")
        login_user(user)
        return redirect(url_for("index"))
    # if not u:
    #     return render_template("auth/login.html", form = form,
    #                             error = "No such email or password!")

    # login_user(user, remember=form.remember_me.data)

    return render_template("auth/login.html", form = form)

@app.route("/auth/logout", methods = ['GET'])
def logout():
    logout_user()
    return redirect(url_for("index"))
