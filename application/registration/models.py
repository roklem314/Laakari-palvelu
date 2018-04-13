from application import db,app
from flask_login import current_user
from application.models import Base

#
# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))

class Users(Base):
    __tablename__ = "account"

    name = db.Column('name', db.String(144), nullable=False)
    address = db.Column('addr', db.String(144), nullable=False)
    postalCode = db.Column('pcode', db.String(144), nullable=False)
    postOffice = db.Column('pOff', db.String(144), nullable = False)
    email = db.Column('email', db.String(25), unique=True)
    password = db.Column('password', db.String())
    appts = db.relationship("Appointment", backref='account', lazy=True)
    role_id= db.Column(db.Integer, db.ForeignKey('role.id'),
                           nullable=True)

    def __init__(self, name, address, postalCode, postOffice,email,password):
        self.name = name
        self.address = address
        self.postalCode = postalCode
        self.postOffice = postOffice
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
