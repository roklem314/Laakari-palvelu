from application import db

class users(db.Model):
    __tablename__ = "user"
    id = db.Column('user_id',db.Integer, primary_key=True)
    name = db.Column('name', db.String(20), nullable=False)
    appt_addr = db.Column('appt_addr', db.String(30), nullable=False)
    role = db.Column('role', db.String(20), nullable=False)
    email = db.Column('email', db.String(20), unique=True, nullable=False)


    def __init__(self,name,appt_addr,role,email):
        self.name = name
        self.appt_addr = appt_addr
        self.role = role
        self.email = email
