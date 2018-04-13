from application import db,app
from flask_login import current_user
from application.models import Base

class Role(Base):
    __tablename__ = "role"

    role = db.Column('role', db.String(144), nullable=False)
    # appt_loc = db.relationship("Appt_location", backref='locations', lazy=True)
    user_role = db.relationship("Users", backref="role", lazy=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
    #                        nullable=True)

    def __init__(self, role):
        self.role = role

# class User_Role(Base):
#
#     location_id = db.Column(db.Integer, db.ForeignKey('location.id'),
#                            nullable=True)
#     appt_id = db.Column(db.Integer, db.ForeignKey('appointment.id'),
#                            nullable=True)
