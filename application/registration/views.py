from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from application import app, db, login_required_role_based
from application.registration.forms import RegistrationForm,ModifyForm,DeleteForm,DoctorRegistrationForm
from application.registration.models import Users
from application.appointment.models import Appointment
from application.role.forms import RoleForm
from application.role.models import Role,user_role
from application.location.forms import LocationForm
from application.location.models import Location
from application.location.models import Base
# import bcrypt

@app.route("/registration/modify_doctor",  methods = ['GET','POST'])
@login_required_role_based('DOCTOR')
def modify_doctor():
    form = ModifyForm()
    form2 = LocationForm()
    if request.method == 'GET':

        u = Users.query.filter_by(id = current_user.id).first()
        u_home = Location.query.filter_by(id = u.loacation_id).first();
        current_user.address = u_home.address
        current_user.postal_code = u_home.postal_code
        current_user.post_office = u_home.post_office

        return render_template("registration/modify_doctor.html", form = ModifyForm(),form2 = LocationForm())

    if request.method == 'POST':
        u = Users.query.filter_by(id = current_user.id).first()
        u_home = Location.query.filter_by(id = u.loacation_id).first();

        if form.validate_on_submit():
            new_name = form.name.data
            new_addr = form2.address.data
            new_postalC = form2.postal_code.data
            new_postF = form2.post_office.data
            new_email = form.email.data
            new_password = form.password.data

            if new_name != u.name:
                u.name = new_name
            if new_addr != u_home.address:
                u_home.address = new_addr
            if new_postalC != u_home.address:
                u_home.postal_code = new_postalC
            if new_postF != u_home.post_office:
                u_home.post_office = new_postF
            if new_email != u.email:
                u.email = new_email
                # if not bcrypt.checkpw(form.password.data.encode("utf-8"), u.password):
                #     u.password = bcrypt.hashpw(form.password.data.encode("utf-8"),bcrypt.gensalt())
            if new_password != u.password:
                u.password = new_password

        db.session.commit()

        flash('Tiedot päivitetty onnistuneesti!')
        return render_template("doctor.html")

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm()
    if Users.query.filter(Users.name == "admin").first() is None:
        admin_role = Role(role="ADMIN")
        db.session.add(admin_role)
        db.session.commit()

        admin = Users(name="admin",email="admin@testi.com",password="admin1234")
        db.session.add(admin)
        db.session.commit()

    if request.method == 'GET':

     return render_template('/registration/register.html',form = RegistrationForm())


    if request.method == 'POST':

        if form.validate_on_submit():

            # u = Users(name=form.name.data, address=form.address.data, email=form.email.data,password = bcrypt.hashpw(form.password.data.encode("utf-8"),bcrypt.gensalt()))
            u_home = Location(address = form.address.data,postal_code= form.postal_code.data,post_office=form.post_office.data)
            db.session.add(u_home)
            db.session.commit()

            u = Users(name=form.name.data,email=form.email.data,password= form.password.data)
            u.loacation_id = u_home.id
            db.session.add(u)
            db.session.commit()

            u_role = Role(role="POTILAS")
            db.session.add(u_role)
            db.session.commit()

            flash('Rekisteröityminen onnistui, voit kirjautua palveluun!')
            return redirect(url_for('login'))
        return render_template('/registration/register.html',form = form)


@app.route('/register/add_new_doctor', methods=['GET', 'POST'])
@login_required_role_based('ADMIN')
def add_new_doctor():
    form = DoctorRegistrationForm()

    if request.method == 'GET':
        return render_template('/registration/register_doctor.html',form = DoctorRegistrationForm())

    if request.method == 'POST':

        if form.validate_on_submit():
            # u = Users(name=form.name.data, address=form.address.data, email=form.email.data,password = bcrypt.hashpw(form.password.data.encode("utf-8"),bcrypt.gensalt()))
            doc_home = Location(address = form.address.data,postal_code= form.postal_code.data,post_office=form.post_office.data)
            db.session.add(doc_home)
            db.session.commit()

            doc = Users(name=form.name.data,email=form.email.data,password = "doctor1234")
            doc.loacation_id = doc_home.id
            db.session.add(doc)
            db.session.commit()

            doc_role = Role(role = "DOCTOR")
            db.session.add(doc_role)
            db.session.commit()

            flash('Uusi lääkäri lisätty palveluun!')
            return redirect(url_for('users_list'))
        return render_template('/registration/register_doctor.html',form = DoctorRegistrationForm())




@app.route("/registration/modify",  methods = ['GET', 'POST'])
@login_required
def modify():
    form = ModifyForm()
    form2 = LocationForm()
    u = Users.query.filter_by(id = current_user.id).first()
    u_home = Location.query.filter_by(id = u.loacation_id).first();
    current_user.address = u_home.address
    current_user.postal_code = u_home.postal_code
    current_user.post_office = u_home.post_office

    if request.method == 'GET':

        return render_template("registration/modify.html", form = ModifyForm(),form2 = LocationForm())

    if request.method == 'POST':
        u = Users.query.filter_by(id = current_user.id).first()
        u_home = Location.query.filter_by(id = u.loacation_id).first();

        if form.validate_on_submit():
            new_name = form.name.data
            new_addr = form2.address.data
            new_postalC = form2.postal_code.data
            new_postF = form2.post_office.data
            new_email = form.email.data
            # password = form.password.data
            # password2 = form.password2.data

            if new_name != u.name:
                u.name = new_name
            if new_addr != u_home.address:
                u_home.address = new_addr
            if new_postalC != u_home.address:
                u_home.postal_code = new_postalC
            if new_postF != u_home.post_office:
                u_home.post_office = new_postF
            if new_email != u.email:
                u.email = new_email
                # if not bcrypt.checkpw(form.password.data.encode("utf-8"), u.password):
                #     u.password = bcrypt.hashpw(form.password.data.encode("utf-8"),bcrypt.gensalt())
            # if new_password != u.password:
            #     u.password = new_password

            db.session.commit()

            flash('Tiedot päivitetty onnistuneesti!')
            return redirect(url_for('index'))

        return render_template("registration/modify.html", form = form,form2 = form2)


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


            db.session.delete(u_home)
            db.session.delete(u)
            db.session.commit()
            flash('Poisto onnistui!')
            return redirect(url_for('logout'))
    return render_template('/registration/delete.html',form = form)
