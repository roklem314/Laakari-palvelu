from flask_wtf import FlaskForm
from wtforms import BooleanField, TextField, validators, StringField,IntegerField
from wtforms.validators import ValidationError, DataRequired


class AppointmentForm(FlaskForm):
    time = StringField("Aika")
    date = StringField("Päivämäärä")
    state = BooleanField("Varaa")

    class Meta:
        csrf = False

class NewAppointmentForm(FlaskForm):
    time = StringField("time", validators=[DataRequired('Time is mandatory!')])
    date = StringField("Date", validators=[DataRequired('Date is mandatory!')])
    address = StringField('Address', validators=[DataRequired('Address is mandatory!')])
    postalCode = StringField('Postalcode',validators=[DataRequired('Postalcode is mandatory!')])
    postOffice = StringField('Postoffice',validators=[DataRequired('Postoffice is mandatory!')])

    class Meta:
        csrf = False
