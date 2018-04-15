from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from application import app,db
from application.registration.forms import RegistrationForm,ModifyForm,DeleteForm
from application.registration.models import Users
from application.appointment.models import Appointment
# from application.role.forms import RoleForm
# from application.role.models import Role
from application.location.forms import LocationForm

# import bcrypt

@app.route('/get_location', methods=['GET', 'POST'])
def get_location():
    form = LocationForm()

    if request.method == 'GET':

     return render_template('/registration/register.html',form = RegistrationForm())


    if request.method == 'POST':

        if form.validate_on_submit():
            # u = Users(name=form.name.data, address=form.address.data, email=form.email.data,password = bcrypt.hashpw(form.password.data.encode("utf-8"),bcrypt.gensalt()))
            u = Users(name=form.name.data,email=form.email.data,address = form.address.data,postalCode = form.postalCode.data, postOffice = form.postOffice.data, password=form.password.data)
            # rooli = form.role.data
            # if null == (Role.query.filter_by(rooli).first()):
            #     new_role = Role(role= rooli)
            #     t.account_id = current_user.id
            #     u.role_id = new_role.id
            #     db.session.add(new_role)
            #     db.session.commit()


            db.session.add(u)
            db.session.commit()

            flash('Rekisteröityminen onnistui, voit kirjautua palveluun!')
            return redirect(url_for('login'))
        return render_template('/registration/register.html',form = form)
