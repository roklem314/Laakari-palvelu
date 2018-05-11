from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from application import app, login_required_role_based
from application.registration.models import Accounts
from application.appointment.models import Appointment
from application.auth.forms import LoginForm,AdministratorLoginForm
from application.location.models import Location
from application.role.models import Role
# import bcrypt

@app.route("/login", methods = ["GET", "POST"])
def login():

    form = LoginForm()
    if request.method == 'GET':
        render_template("auth/login.html", form = form)

    if request.method == 'POST':
        if form.validate_on_submit():
            u = Accounts.query.filter_by(email=form.email.data).first()
            # # if u is None or not bcrypt.checkpw(form.password.data.encode("utf-8"), u.password):
            if u.password != form.password.data:

                return render_template("auth/login.html", form = form)

            if any('DOCTOR' in s for s in Accounts.roles(form.email.data)):
                login_user(u)
                return redirect(url_for("doctor"))
            else:
                login_user(u)
                return redirect(url_for("index"))


    return render_template("auth/login.html", form = form)

@app.route("/auth/login_admin", methods = ["GET","POST"])
def administrator():

    form = AdministratorLoginForm()
    if request.method == 'GET':
        render_template("auth/login_admin.html", form = form)

    if request.method == 'POST':
        if form.username.data == "admin_fullcare" and form.password.data == "3.14159265359":
            adm = Accounts.query.filter(Accounts.email == "adm@testi.com").first()
            login_user(adm)
            return render_template("author.html",)

    return render_template("auth/login_admin.html", form = form)

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
