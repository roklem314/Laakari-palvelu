from application import app, db
from flask import redirect, render_template, request, url_for,flash
from application.tasks.models import users



@app.route("/laakarit", methods=["GET"])
def laakarit():
    return render_template("tasks/list.html", users = users.query.all())



@app.route('/uusi_asiakas', methods = ['GET', 'POST'])
def uusi_asiakas():
   if request.method == 'POST':
        if request.form['name'] != "" and request.form['appt_addr'] != "" and request.form['role'] != "" and request.form['email'] != "":
            newuser = users(request.form['name'], request.form['appt_addr'],request.form['role'],request.form['email'])
            db.session.add(newuser)
            db.session.commit()

            flash('Uusi lääkäri lisätty!')
            return redirect( url_for('laakarit'))
        flash('Lääkärin lisäys epäonnistui, tarkista annoitko pakolliset tiedot!')
   return render_template('/tasks/new.html')


@app.route("/modify", methods=['GET','POST'])
def update_user():
    if request.method == 'POST':
        uid = request.form['uid']
        new_name = request.form['name']
        new_addr = request.form['appt_addr']
        new_role = request.form['role']
        new_email = request.form['email']
        user = users.query.filter_by(id = uid).first()
        if new_name != "":
            user.name = new_name
        if new_addr != "":
            user.appt_addr = new_addr
        if new_role != "":
            user.role = new_role
        if new_email != "":
            user.email = new_email

        db.session.commit()
        flash('Päivitys onnistui!')
        return redirect( url_for('laakarit'))

    return redirect( url_for('laakarit'))

@app.route("/muokkaa/<int:uid>", methods=["GET"])
def muokkaa(uid: int):
    user = users.query.filter_by(id = uid).first()

    return render_template("tasks/modify.html", user=user)

@app.route("/delete", methods=["POST"])
def delete():
    uid = request.form['uid']
    user = users.query.filter_by(id = uid).first()
    db.session.delete(user)
    db.session.commit()
    flash('Poisto onnistui!')
    return redirect(url_for('laakarit'))
