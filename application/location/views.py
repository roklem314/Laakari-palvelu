from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from application import app,db
from application.registration.forms import RegistrationForm,ModifyForm,DeleteForm
from application.registration.models import Accounts
from application.appointment.models import Appointment
from application.location.forms import LocationForm

@app.route('/get_location', methods=['GET', 'POST'])
def get_location():
    form = LocationForm()

    if request.method == 'GET':

     return render_template('/registration/register.html',form = RegistrationForm())


    if request.method == 'POST':

        if form.validate_on_submit():
            u = Accounts(name=form.name.data,email=form.email.data,address = form.address.data,postal_code = form.postal_code.data, post_office = form.post_office.data, password=form.password.data)
            db.session.add(u)
            db.session.commit()

            flash('Rekisteröityminen onnistui, voit kirjautua palveluun!')
            return redirect(url_for('login'))
        return render_template('/registration/register.html',form = form)
