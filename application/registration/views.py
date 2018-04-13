from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from application import app,db
from application.registration.forms import RegistrationForm,ModifyForm,DeleteForm
from application.registration.models import Users
from application.appointment.models import Appointment
from application.role.forms import RoleForm
from application.role.models import Role
# import bcrypt

@app.route('/register', methods=['GET', 'POST'])
def register_user():

    form = RegistrationForm()

    if form.validate_on_submit():


        # u = Users(name=form.name.data, address=form.address.data, email=form.email.data,password = bcrypt.hashpw(form.password.data.encode("utf-8"),bcrypt.gensalt()))
        u = Users(name=form.name.data,email=form.email.data,address = form.address.data,postalCode = form.postalCode.data, postOffice = form.postOffice.data, password=form.password.data)
        db.session.add(u)
        db.session.commit()

        # u.set_password(form.password.data)
        # db.session.add(u)
        # db.session.commit()

        flash('Rekisteröityminen onnistui, voit kirjautua palveluun!')
        return redirect(url_for('login'))

    return render_template('/registration/register.html', form=form)


@app.route("/registration/modify",  methods = ['GET', 'POST'])
@login_required
def modify():
    form = ModifyForm()

    if form.validate_on_submit():
        new_name = form.name.data
        new_addr = form.address.data
        new_postalC = form.postalCode.data
        new_postF = form.postOffice.data
        new_email = form.email.data
        new_password = form.password.data

        u = Users.query.filter_by(id = current_user.id).first()

        if new_name != current_user.name:
            u.name = new_name
        if new_addr != current_user.address :
            current_user.address = new_addr
        if new_postalC != current_user.postalCode:
            current_user.postalCode = new_postalC
        if new_postF != current_user.postOffice:
            current_user.postOffice != current_user.postOffice
        if new_email != current_user.email:
            u.email = new_email
        # if not bcrypt.checkpw(form.password.data.encode("utf-8"), u.password):
        #     u.password = bcrypt.hashpw(form.password.data.encode("utf-8"),bcrypt.gensalt())
        if new_password != current_user.password:
            u.password = new_password

        db.session.commit()

        flash('Tiedot päivitetty onnistuneesti!')
        return redirect(url_for('index'))

    return render_template("registration/modify.html", form = form )

@app.route("/registration/delete_user", methods = ['GET','POST'])
@login_required
def delete_user():

    form = DeleteForm()

    if form.validate_on_submit():

        u = Users.query.filter_by(id = current_user.id).first()
        omat = Appointment.query.filter(current_user.id == Appointment.account_id).all()

        for o in omat:
            t = Appointment.query.get(o.id)
            t.state = False
            t.account_id = None
            db.session().commit()

        db.session.delete(u)
        db.session.commit()
        flash('Poisto onnistui!')

        return redirect(url_for('logout'))

    # flash('Käyttätietojen poisto, vahvistetaan syöttämällä voimassa oleva salasana!')
    return render_template("registration/delete.html", form = form)
