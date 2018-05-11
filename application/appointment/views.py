from application import app, db, login_required_role_based
from flask import Flask, redirect, render_template, request, url_for,redirect, flash
from flask_login import login_required, current_user
from application.appointment.models import Appointment
from application.appointment.forms import AppointmentForm,NewAppointmentForm,DoctorAppointmentForm
from application.registration.models import Accounts
from application.location.forms import LocationForm
from application.location.models import Location


@app.route("/appointment/info/<int:uid>", methods=['GET', 'POST'])
@login_required_role_based('PATIENT')
def info(uid: int):

    if request.method == 'POST':
        return redirect(url_for("appts_list"))

    t = Appointment.query.get(uid)
    id = t.location_id

    return render_template("appointment/info.html",t_location = Location.find_appt_loacation(id))

@app.route("/appointment/list", methods=["GET"])
@login_required_role_based('PATIENT')
def appts_list():
    u = Accounts.query.filter_by(id = current_user.id).first()
    u_home = Location.query.filter_by(id = u.loacation_id).first();
    u_post_office = u_home.post_office
    print(u_post_office)
    nearest_locations = Location.list_nearest_locations(u_post_office)
    print(nearest_locations)
    if nearest_locations is None:
        return render_template("appointment/list.html", appts = Appointment.query.all())
    return render_template("appointment/list.html", appts = Appointment.query.all(), nearest_locations=nearest_locations)

@app.route("/appointment/appts_doctor", methods=["GET"])
@login_required_role_based('DOCTOR')
def appts_doctor():

    return render_template("/appointment/appts_doctor.html",appts = Appointment.query.all())

@app.route("/appointment/appts_list_all", methods=["GET"])
@login_required_role_based('ADMIN')
def appts_list_all():
    all_appts_and_locations = Location.find_all_appts_and_locations()

    return render_template("appointment/appts_list_all.html",all_appts_and_locations = all_appts_and_locations)

@app.route("/appointment/my_appt", methods=["GET"])
@login_required
def appts_own():

    return render_template("appointment/my_appt.html", my_appt_appts = Appointment.query.filter(current_user.id == Appointment.account_id).all())

@app.route("/appointment/book/<int:uid>", methods=['GET','POST'])
@login_required_role_based('PATIENT')
def book(uid: int):

    t = Appointment.query.get(uid)
    t.state = True
    t.account_id = current_user.id
    db.session().commit()

    return redirect(url_for("appts_list"))

@app.route("/appointment/cancel_booking/<int:uid>", methods=['GET','POST'])
@login_required_role_based('PATIENT')
def cancel_booking(uid: int):
    t = Appointment.query.get(uid)
    t.state = False
    t.account_id = None
    db.session().commit()

    return redirect(url_for("appts_own"))

@app.route("/appointment/add_new_appt", methods=['GET','POST'])
@login_required_role_based('ADMIN')
def add_new_appt():
    form = NewAppointmentForm()

    if request.method == 'GET':

        return render_template("appointment/add_new_appt.html", form = form)

    if request.method == 'POST':

        new_appt= Appointment(form.time.data, form.date.data,False)
        new_location = Location(form.address.data, form.postal_code.data, form.post_office.data)
        db.session().add(new_location)
        db.session().commit()

        new_appt.location_id = new_location.id
        db.session().add(new_appt)
        db.session().commit()
    flash('New appointment added!')
    return redirect(url_for('appts_list_all'))
