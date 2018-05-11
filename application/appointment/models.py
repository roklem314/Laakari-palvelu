from application import db,app
from application.models import Base

class Appointment(Base):

    __tablename__ = "appointment"

    time = db.Column(db.String(5), nullable=False)
    date = db.Column(db.String(10), nullable = False)
    state = db.Column(db.Boolean, default=False, nullable = False)
    doctor = db.Column(db.String(20),nullable=True)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'),
                           nullable=True)
    def __init__(self,time,date,doctor):
        self.time = time
        self.date = date

    def get_id(self):
        return self.id
