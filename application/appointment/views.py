from application import app, db
from flask import Flask, redirect, render_template, request, url_for,redirect, flash
from flask_login import login_required, current_user

from application.appointment.models import Appointment
from application.appointment.forms import AppointmentForm
from application.registration.models import Users

@app.route("/appointment/list", methods=["GET"])
@login_required
def appts_list():

    return render_template("appointment/list.html", appts = Appointment.query.all())

@app.route("/appointment/addnew", methods=['GET'])
@login_required
def appt_form():

    return render_template("appointment/addnew.html", form = AppointmentForm())

@app.route("/appointment/varaa/<int:uid>", methods=['GET','POST'])
@login_required
def varaa(uid: int):

    t = Appointment.query.get(uid)
    t.state = True
    t.account_id = current_user.id
    db.session().commit()

    return redirect(url_for("appts_list"))

@app.route("/appointment/peru/<int:uid>", methods=['GET','POST'])
@login_required
def peru(uid: int):
    t = Appointment.query.get(uid)
    t.state = False
    t.account_id = None
    db.session().commit()

    return redirect(url_for("varaukset"))

@app.route("/appointment/", methods=["POST"])
@login_required
def new_appt():
    form = AppointmentForm(request.form)

    a = Appointment(form.time.data, form.date.data)
    # a.account_id = current_user.id

    # if not form.validate():
    #     return render_template("appointment/addnew.html", form = form)



    db.session().add(a)
    db.session().commit()

    return redirect(url_for('appts_list'))

@app.route("/appointment/omat",methods= ['GET'])
@login_required
def varaukset():

    return render_template("appointment/omat.html", omat = Appointment.query.filter(current_user.id == Appointment.account_id).all())
