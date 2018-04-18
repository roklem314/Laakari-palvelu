from application import db,app
from flask_login import current_user
from application.models import Base
from sqlalchemy.sql import text

#
# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))

class Location(Base):
    __tablename__ = "location"

    address = db.Column('address', db.String(144), nullable=False)
    postalCode = db.Column('postalCode', db.Integer(), nullable=False)
    postOffice = db.Column('postOffice', db.String(144), nullable = False)

    u_location = db.relationship("Users", backref='loacation', lazy=True)

    appts_location = db.relationship("Appointment", backref='location', lazy=True)

    def __init__(self,address, postalCode, postOffice):

        self.address = address
        self.postalCode = postalCode
        self.postOffice = postOffice

    def get_id(self):
        return self.id

    @staticmethod
    def find_appt_loacation(id):
        stmt = text("SELECT Appointment.id,Appointment.time, Appointment.date, Appointment.state, Location.address, Location.postalCode, Location.postOffice FROM Location,Appointment"
                    " WHERE (Location.id = Appointment.location_id) AND (Appointment.location_id = :id)").params(id=id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0],"time":row[1], "date":row[2],"state":row[3],"address":row[4], "postalCode":row[5],"postOffice":row[6]})

        return response
    @staticmethod
    def list_nearest_locations(u_postOffice):
        stmt = text("SELECT Appointment.id,Appointment.time, Appointment.date,Location.postOffice FROM Location,Appointment").params(u_postOffice=u_postOffice)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0],"time":row[1], "date":row[2],"postOffice":row[3]})
