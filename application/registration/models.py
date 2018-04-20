from application import db,app
from flask_login import current_user
from application.models import Base
from application.role.forms import RoleForm
from application.role.models import Role



#
# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))

class Users(Base):
    __tablename__ = "account"

    name = db.Column('name', db.String(144), nullable=False)
    email = db.Column('email', db.String(25), unique=True)
    password = db.Column('password', db.String())
    appts = db.relationship("Appointment", backref='account', lazy=True)
    loacation_id= db.Column(db.Integer, db.ForeignKey('location.id'),
                           nullable=True)
    role = db.relationship("User_Role",backref = 'account',lazy = True)

    def __init__(self, name,email,password):
        self.name = name
        self.email = email
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


    # def set_password(self, password):
    #     self.password = generate_password_hash(password)
    #
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password, password)
