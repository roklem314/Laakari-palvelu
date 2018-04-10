from application import db,app
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user




#
# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))

class Users(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    # date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    # date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    #                           onupdate=db.func.current_timestamp())

    name = db.Column('name', db.String(144), nullable=False)
    address = db.Column('address', db.String(30), nullable=False)
    email = db.Column('email', db.String(25), unique=True)
    password = db.Column('password', db.String())


    appts = db.relationship("Appointment", backref='account', lazy=True)

    def __init__(self, name, address, email,password):
        self.name = name
        self.address = address
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
