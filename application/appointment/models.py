from application import db,app

class Appointment(db.Model):

    __tablename__ = "appointment"
    id = db.Column(db.Integer, primary_key=True)
    # date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    # date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    # onupdate=db.func.current_timestamp())

    # patient_idenity = db.Column('patient_idenity', db.String(30),nullable=False)
    # diagnos = db.Column('diagnos', db.String(16), nullable=False)
    # operation= db.Column('operation',db.String(16), nullable=False)
    # info = db.Column('info', db.String(200), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id') )

    time = db.Column(db.String(5), nullable=False)
    date = db.Column(db.String(10), nullable = False)
    state = db.Column(db.Boolean, default=False, nullable = False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=True)

    def __init__(self,time,date):
        self.time = time
        self.date = date

    def get_id(self):
        return self.id
