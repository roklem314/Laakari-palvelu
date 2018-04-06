from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from application import app,db
from application.registration.forms import RegistrationForm,ModifyForm,DeleteForm
from application.registration.models import Users
from application.appointment.models import Appointment
import bcrypt

@app.route('/register', methods=['GET', 'POST'])
def register_user():

    form = RegistrationForm()

    if form.validate_on_submit():

        user = Users(name=form.name.data, address=form.address.data, email=form.email.data, password = bcrypt.hashpw(form.password.data.encode("utf-8"),bcrypt.gensalt()))
        # user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Rekisteröityminen onnistui, voit kirjautua palveluun!')
        return redirect(url_for('login'))

    return render_template('/registration/register.html', form=form)

# @app.route('/layout', methods = ['GET'])
# def reg_u():
#     form = RegistrationForm()
#     return render_template('/registration/register.html', form=form)

@app.route("/registration/modify",  methods = ['GET', 'POST'])
@login_required
def modify():
    form = ModifyForm()

    if form.validate_on_submit():
        new_name = form.name.data
        new_addr = form.address.data
        new_email = form.email.data
        new_password = form.password.data
        user = Users.query.filter_by(id = current_user.id).first()
        if new_name != "":
            user.name = new_name
        if new_addr != "" :
            user.address = new_addr
        if new_email != "" or new_email != current_user.email:
            user.email = new_email
        if new_password != "" or new_password != current_user.password:
            password = bcrypt.hashpw(form.password.data.encode("utf-8"),bcrypt.gensalt())

        db.session.commit()

        flash('Tiedot päivitetty onnistuneesti!')
        return redirect(url_for('index'))

    return render_template("registration/modify.html", form = form)

@app.route("/registration/delete_user", methods = ['GET','POST'])
@login_required
def delete_user():

    form = DeleteForm()
    # if request.method == 'POST':
    if form.validate_on_submit():

        user = Users.query.filter_by(id = current_user.id).first()
        omat = Appointment.query.filter(current_user.id == Appointment.account_id).all()

        for o in omat:
            t = Appointment.query.get(o.id)
            t.state = False
            t.account_id = None
            db.session().commit()

        db.session.delete(user)
        db.session.commit()
        flash('Poisto onnistui!')

        return redirect(url_for('logout'))

    # flash('Käyttätietojen poisto, vahvistetaan syöttämällä voimassa oleva salasana!')
    return render_template("registration/delete.html", form = form)
