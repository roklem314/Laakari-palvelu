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
        stmt = text("SELECT Appointment.id,Appointment.time, Appointment.date,Appointment.state FROM Location,Appointment"
                    " WHERE (Location.id = Appointment.location_id) AND (Location.postOffice == :u_postOffice) ").params(u_postOffice = u_postOffice)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0],"time":row[1], "date":row[2],"state":row[3]})
        return response

    @staticmethod
    def find_all_users_with_locations(author_email):
        stmt = text("SELECT account.name,account.email, Location.address, Location.postalCode, Location.postOffice ,Role.role FROM Location,account,Role"
                    " WHERE (Location.id = account.id) AND (Role.id = account.id) AND (account.email != :author_email) ").params(author_email=author_email)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"name":row[0],"email":row[1],"address":row[2],"postalCode":row[3],"postOffice":row[4],"role":row[5]})

        return response
    @staticmethod
    def find_all_appts_and_locations():
        stmt = text("SELECT Appointment.time, Appointment.date, Appointment.state, Location.address,Location.postalCode,Location.postOffice FROM Location,Appointment"
                    " WHERE (Location.id = Appointment.location_id)" )
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"time":row[0], "date":row[1],"state":row[2],"address":row[3],"postalCode":row[4],"postOffice":row[5]})

        return response
