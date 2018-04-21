from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from application import app,db
from application.registration.forms import RegistrationForm,ModifyForm,DeleteForm
from application.registration.models import Users
from application.appointment.models import Appointment
from application.role.forms import RoleForm
from application.role.models import Role
from application.location.forms import LocationForm
from application.location.models import Location
from application.location.models import Base
# import bcrypt

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm()

    if request.method == 'GET':

     return render_template('/registration/register.html',form = RegistrationForm())


    if request.method == 'POST':

        if form.validate_on_submit():
            # u = Users(name=form.name.data, address=form.address.data, email=form.email.data,password = bcrypt.hashpw(form.password.data.encode("utf-8"),bcrypt.gensalt()))
            u_home = Location(address = form.address.data,postalCode= form.postalCode.data,postOffice=form.postOffice.data)
            db.session.add(u_home)
            db.session.commit()

            u = Users(name=form.name.data,email=form.email.data,password= form.password.data)
            u.loacation_id = u_home.id
            db.session.add(u)
            db.session.commit()

            u_role = Role(role = form.role.data)
            db.session.add(u_role)
            db.session.commit()
            # u_home.u_location = u.id

            db.session.commit()


            flash('Rekisteröityminen onnistui, voit kirjautua palveluun!')
            return redirect(url_for('login'))
        return render_template('/registration/register.html',form = form)


@app.route("/registration/modify",  methods = ['GET', 'POST'])
@login_required
def modify():
    form = ModifyForm()
    form2 = LocationForm()
    if request.method == 'GET':

        u = Users.query.filter_by(id = current_user.id).first()
        u_home = Location.query.filter_by(id = u.loacation_id).first();
        current_user.address = u_home.address
        current_user.postalCode = u_home.postalCode
        current_user.postOffice = u_home.postOffice


        return render_template("registration/modify.html", form = ModifyForm(),form2 = LocationForm())

    if request.method == 'POST':
        u = Users.query.filter_by(id = current_user.id).first()
        u_home = Location.query.filter_by(id = u.loacation_id).first();

        if form.validate_on_submit():
            new_name = form.name.data
            new_addr = form2.address.data
            new_postalC = form2.postalCode.data
            new_postF = form2.postOffice.data
            new_email = form.email.data
            new_password = form.password.data

            if new_name != u.name:
                u.name = new_name
            if new_addr != u_home.address:
                u_home.address = new_addr
            if new_postalC != u_home.address:
                u_home.postalCode = new_postalC
            if new_postF != u_home.postOffice:
                u_home.postOffice = new_postF
            if new_email != u.email:
                u.email = new_email
                # if not bcrypt.checkpw(form.password.data.encode("utf-8"), u.password):
                #     u.password = bcrypt.hashpw(form.password.data.encode("utf-8"),bcrypt.gensalt())
            if new_password != u.password:
                u.password = new_password

        db.session.commit()

        flash('Tiedot päivitetty onnistuneesti!')
        return redirect(url_for('index'))


@app.route("/registration/delete_user", methods = ['GET','POST'])
@login_required
def delete_user():

    form = DeleteForm()
    if request.method == 'GET':
        return render_template("registration/delete.html", form = DeleteForm())

    if request.method == 'POST':
        if form.validate_on_submit():

            u = Users.query.filter_by(id = current_user.id).first()
            omat = Appointment.query.filter(current_user.id == Appointment.account_id).all()
            u_home = Location.query.filter_by(id = u.loacation_id).first();


            for o in omat:
                t = Appointment.query.get(o.id)
                t.state = False
                t.account_id = None
                db.session().commit()


            db.sesion.delete(u_home)
            db.session.delete(u)
            db.session.commit()
            flash('Poisto onnistui!')

        return redirect(url_for('logout'))

# @app.route('/user_info', methods=['GET'])
# def user_info():
#     omat = Appointment.query.filter(current_user.id == Appointment.account_id).all()
#     u_home = Location.query.filter(Users.id == u.loacation_id).first();
#     # role = Role.query.filter(Role.id == current_user.id).first()
#
#     return render_template('/registration/user_info.html',omat,u_home)
