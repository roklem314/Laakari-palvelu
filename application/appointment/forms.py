from flask_wtf import FlaskForm
from wtforms import BooleanField, TextField, validators, StringField, RadioField

class AppointmentForm(FlaskForm):
    time = StringField("Aika")
    date = StringField("Pvm")
    state = BooleanField("Varaa")

    class Meta:
        csrf = False
