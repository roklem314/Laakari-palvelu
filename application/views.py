from flask import render_template
from application import app,db
from application.registration.models import Accounts
from application.role.models import Role
from flask_login import login_required, current_user

@app.route("/")
def index():
    # adm = Accounts(name="administrator",email="adm@testi.com",password="3.14159265359")
    # adm_role = Role(role="ADMIN")
    # db.session.add(adm_role)
    # db.session.add(adm)
    # db.session.commit()

    return render_template("index.html")
@app.route("/author")
@login_required
def author():
    return render_template("author.html")
@app.route("/doctor")
@login_required
def doctor():
    return render_template("doctor.html")
