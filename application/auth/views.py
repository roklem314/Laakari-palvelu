from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from application import app, login_required_role_based
from application.registration.models import Users
from application.appointment.models import Appointment
from application.auth.forms import LoginForm
from application.location.models import Location
from application.role.models import Role
# import bcrypt

@app.route("/login", methods = ["GET", "POST"])
def login():
    
    form = LoginForm()

    if form.validate_on_submit():
        u = Users.query.filter_by(email=form.email.data).first()
        # # if u is None or not bcrypt.checkpw(form.password.data.encode("utf-8"), u.password):
        if u.password != form.password.data:

            return render_template("auth/login.html", form = form)

        if any('ADMIN' in s for s in Users.roles(form.email.data)):
            login_user(u)
            return render_template("author.html")
        if any('DOCTOR' in s for s in Users.roles(form.email.data)):
            login_user(u)
            return render_template("doctor.html")
        else:
            login_user(u)
            return redirect(url_for("index"))


    return render_template("auth/login.html", form = form)

@app.route("/auth/logout", methods = ['GET'])
def logout():
    logout_user()
    flash("Logout successful!")
    return redirect(url_for("index"))

@app.route("/auth/users_list", methods = ["GET"])
@login_required_role_based('ADMIN')
def users_list():
    u_all = Location.find_all_users_with_locations(current_user.email)
    return render_template("auth/users_list.html",u_all=u_all)
