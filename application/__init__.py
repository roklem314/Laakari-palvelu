# flask-sovellus
from flask import Flask
# from flask import Flask, render_template
# from flask_bootstrap import Bootstrap

app = Flask(__name__)
# bootstrap = Bootstrap(app)




# tietokanta
from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kanta.db"
    app.config["SQLALCHEMY_ECHO"] = True


db = SQLAlchemy(app)

# oman sovelluksen toiminnallisuudet
from application import views

from application.appointment import models
from application.appointment import views

from application.auth import views

from application.location import models
from application.location import views

from application.registration import models
from application.registration import views



# from application.role import models
# from application.role import views

# rekisteroituminen
from application.registration.models import Users
from os import urandom
app.config["SECRET_KEY"] = urandom(42)

from flask_login import LoginManager,current_user


login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Please login to use this functionality."

# roles in login_required
from functools import wraps
def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
                return login_manager.unauthorized()

            unauthorized = False

            if role != "ANY":
                unauthorized = True

                for user_role in current_user.roles():
                    if user_role == role:
                        unauthorized = False
                        break

            if unauthorized:
                return login_manager.unauthorized()

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

# luodaan taulut tietokantaan tarvittaessa
try:
    db.create_all()
except:
    pass
