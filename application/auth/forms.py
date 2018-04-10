from flask_wtf import FlaskForm
from wtforms import PasswordField, TextField, StringField
from wtforms.validators import ValidationError, DataRequired, Email
from application.registration.models import Users
# import bcrypt

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Sähköposti on pakollinnen!"), Email("Tarkista sähköposti osoite!")])
    password = PasswordField("Salasana", validators=[DataRequired("Salasana on pakollinnen!")])

    def validate_email_password(self, email,password):
        u = Users.query.filter_by(email=email.data).first()
        if u is None:
            raise ValidationError('Sähköposti osoite on virheellinen!.')
        if u.password != password.data:
        # if not bcrypt.checkpw(password.data.encode("utf-8"), u.password)
            raise ValidationError('Salasanan on virheellinen!')
    # def validate_password(self, password):
    #     u = Users.query.filter_by(id = c).first()
    #     if  0 == u.check_password(password.data):
    #         raise ValidationError('Salasanan on virheellinen!')



    class Meta:
        csrf = False
