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
         return redirect( url_for('index'))

   return render_template("tasks/new.html")

@app.route("/update", methods=["POST"])
def update():
    newemail = request.form.get("new_email")
    oldemail = request.form.get("old_email")
    user = users.query.filter_by(email=oldemail).first()
    user.email = newemail
    db.session.commit()

    return redirect( url_for('list_all'))

@app.route("/delete", methods=["POST"])
def delete():
    userid = request.form.get("id")
    user = users.query.filter_by(id=userid).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_all'))
