from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField,IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from application.registration.models import Users
# import bcrypt


class LocationForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired('Address is mandatory!')])
    postal_code = StringField('Postalcode',validators=[DataRequired('Postalcode is mandatory!')])
    post_office = StringField('Postoffice',validators=[DataRequired('Postoffice is mandatory!')])

    class Meta:
        csrf = False
