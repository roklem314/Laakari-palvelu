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
    time = StringField("Aika")
    date = StringField("Päivämäärä")
    address = StringField('Osoite',validators=[DataRequired("Osoite on pakollinen")])
    postalCode = IntegerField('Postinumero',validators=[DataRequired("Postinumero on pakollinen")])
    postOffice = StringField('Postitoimipaikka',validators=[DataRequired("Postitoimipaikka on pakollinen")])

    class Meta:
        csrf = False
