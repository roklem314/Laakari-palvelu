# flask-sovellus
from flask import Flask

app = Flask(__name__)


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

# from application.auth import models
from application.auth import views

from application.registration import models
from application.registration import views

# rekisteroituminen
from application.registration.models import Users
from os import urandom
app.config["SECRET_KEY"] = urandom(42)

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

# luodaan taulut tietokantaan tarvittaessa
try:
    db.create_all()
except:
    pass
