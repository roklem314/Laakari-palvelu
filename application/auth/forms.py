from flask_wtf import FlaskForm
from wtforms import PasswordField, TextField, StringField
from wtforms.validators import ValidationError, DataRequired, Email
from application.registration.models import Users

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Sähköposti on pakollinnen!"), Email("Tarkista sähköposti osoite!")])
    password = PasswordField("Salasana")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Sähköposti osoite on virheellinen!.')



    class Meta:
        csrf = False
