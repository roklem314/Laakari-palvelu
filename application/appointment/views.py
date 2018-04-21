from application import app, db
from flask import Flask, redirect, render_template, request, url_for,redirect, flash
from flask_login import login_required, current_user

from application.appointment.models import Appointment
from application.appointment.forms import AppointmentForm,NewAppointmentForm
from application.registration.models import Users

from application.location.forms import LocationForm
from application.location.models import Location

@app.route("/appointment/info/<int:uid>", methods=['GET', 'POST'])
@login_required
def info(uid: int):

    if request.method == 'POST':
        return redirect(url_for("appts_list"))

    t = Appointment.query.get(uid)
    # t_location = Location.find_appt_loacation(t.location_id)
    id = t.location_id


    return render_template("appointment/info.html",t_location = Location.find_appt_loacation(id))


@app.route("/appointment/list", methods=["GET"])
@login_required
def appts_list():
    u = Users.query.filter_by(id = current_user.id).first()
    u_home = Location.query.filter_by(id = u.loacation_id).first();
    u_postOffice = u_home.postOffice
    print(u_postOffice)
    nearest_locations = Location.list_nearest_locations(u_postOffice)
    print(nearest_locations)
    # nearest_locations = Location.query.filter(Location.postOffice == u_postOffice,Location.id == Appointment.location_id).all()
    if nearest_locations is None:
        return render_template("appointment/list.html", appts = Appointment.query.all())
    return render_template("appointment/list.html", appts = Appointment.query.all(), nearest_locations=nearest_locations)

@app.route("/author/appts_list_all", methods=["GET"])
@login_required
def appts_list_all():
    all_appts_and_locations = Location.find_all_appts_and_locations()

    return render_template("appointment/appts_list_all.html",all_appts_and_locations = all_appts_and_locations)



@app.route("/appointment/omat", methods=["GET"])
@login_required
def appts_own():

    return render_template("appointment/omat.html", omat_appts = Appointment.query.filter(current_user.id == Appointment.account_id).all())

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

#
# @app.route("/appointment/addnew", methods=['GET'])
# @login_required
# def appt_form():
#
#     return render_template("appointment/addnew.html", form = AppointmentForm())

@app.route("/appointment/add_new_appt", methods=['GET','POST'])
@login_required
def add_new_appt():
    form = NewAppointmentForm()

    if request.method == 'GET':

        return render_template("appointment/add_new_appt.html", form = form)

    if request.method == 'POST':

        new_appt= Appointment(form.time.data, form.date.data,False)
        new_location = Location(form.address.data, form.postalCode.data, form.postOffice.data)
        db.session().add(new_location)
        db.session().commit()

        new_appt.location_id = new_location.id
        db.session().add(new_appt)
        db.session().commit()

    return redirect(url_for('appts_list_all'))

@app.route("/appointment/omat",methods= ['GET'])
@login_required
def varaukset():

    return render_template("appointment/omat.html", omat = Appointment.query.filter(current_user.id == Appointment.account_id).all())
