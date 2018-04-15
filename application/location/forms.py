from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField,SubmitField,RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from application.registration.models import Users
# import bcrypt


class LocationForm(FlaskForm):
    address = StringField('Osoite',validators=[DataRequired("Osoite on pakollinen")])
    postalCode = StringField('Postinumero',validators=[DataRequired("Postinumero on pakollinen")])
    postOffice = StringField('Postitoimipaikka',validators=[DataRequired("Postitoimipaikka on pakollinen")])

    class Meta:
        csrf = False
