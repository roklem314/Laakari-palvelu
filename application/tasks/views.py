from application import app, db
from flask import redirect, render_template, request, url_for,flash
from application.tasks.models import users



@app.route("/list_all", methods=["GET"])
def list_all():
    return render_template("tasks/list.html", users = users.query.all())


@app.route("/tasks/new", methods=["GET"])
def new_user():
        return render_template("tasks/new.html")

@app.route('/new', methods = ['GET', 'POST'])
def create_user():
   if request.method == 'POST':
         newuser = users(request.form['name'], request.form['appt_addr'],request.form['role'],request.form['email'])
         db.session.add(newuser)
         db.session.commit()

         flash('Record was successfully added')
         return redirect( url_for('list_all'))

   return render_template("tasks/new.html")

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

        return redirect( url_for('list_all'))

    return redirect( url_for('list_all'))

@app.route("/update/<int:uid>", methods=["GET"])
def update(uid: int):
    user = users.query.filter_by(id = uid).first()
    return render_template("tasks/modify.html", user=user)

@app.route("/delete", methods=["POST"])
def delete():
    uid = request.form['uid']
    user = users.query.filter_by(id = uid).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_all'))
