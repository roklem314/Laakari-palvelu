from flask_wtf import FlaskForm
from wtforms import BooleanField, TextField, validators, StringField,IntegerField
from wtforms.validators import ValidationError, DataRequired

class DoctorAppointmentForm(FlaskForm):
    time = StringField("Time")
    date = StringField("Date")
    state = BooleanField("Book")
    doctor = StringField("Doctor")

    class Meta:
        csrf = False

class AppointmentForm(FlaskForm):
    time = StringField("Time")
    date = StringField("Date")
    state = BooleanField("Book")

    class Meta:
        csrf = False

class NewAppointmentForm(FlaskForm):
    time = StringField("Time", validators=[DataRequired('Time is mandatory!')])
    date = StringField("Date", validators=[DataRequired('Date is mandatory!')])
    address = StringField('Address', validators=[DataRequired('Address is mandatory!')])
    postal_code = StringField('Postalcode',validators=[DataRequired('Postalcode is mandatory!')])
    post_office = StringField('Postoffice',validators=[DataRequired('Postoffice is mandatory!')])

    class Meta:
        csrf = False
