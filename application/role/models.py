from application import db,app
from flask_login import current_user
from application.models import Base

class Role(Base):
    __tablename__ = "role"

    role = db.Column('role', db.String(144), nullable=False)
    user_role = db.relationship("user_role", backref="role", lazy=True)


    def __init__(self, role):
        self.role = role

class user_role(Base):

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'),
                           nullable=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=True)
