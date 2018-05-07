import os
import random
from functools import wraps
from flask import Flask
from flask_login import LoginManager,current_user
from os import urandom
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

if os.environ.get("HEROKU"): #running at HEROKU
    app.config["SECRET_KEY"] = random.getrandbits(420)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_ECHO"] = False

else: #running at LOCALHOST
    app.config["SECRET_KEY"] = urandom(42)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kanta.db"
    app.config["SQLALCHEMY_ECHO"] = True

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

# roles in login_required
def login_required_role_based(role):
	def wrapper(fn):
		@wraps(fn)
		def decorated_view(*args, **kwargs):

			if not current_user.is_authenticated:
				return login_manager.unauthorized()

			if not any(role in s for s in current_user.roles(current_user.email)):
				return login_manager.unauthorized()

			return fn(*args, **kwargs)

		return decorated_view

	return wrapper

# needed imports to use app
from application import views

from application.appointment import models
from application.appointment import views
from application.auth import views
from application.location import models
from application.location import views
from application.registration import models
from application.registration import views
from application.role import models
from application.role import views
from application.registration.models import Users

# luodaan taulut tietokantaan tarvittaessa ja
if not os.environ.get("HEROKU"):
    try:
        db.create_all()
    except:
        pass
