from flask_wtf import FlaskForm
from wtforms import PasswordField, TextField, StringField
from wtforms.validators import ValidationError, DataRequired, Email
from application.registration.models import Users
# import bcrypt

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Please check your email!')])
    password = PasswordField('Password', validators=[DataRequired('Password is mandatory!')])

    def validate_email(self, email):
        u = Users.query.filter_by(email=email.data).first()
        if u is None:
            raise ValidationError('E-mail address is incorrect or does not exist!')
        # if u.password != password.data:
        # # if not bcrypt.checkpw(password.data.encode("utf-8"), u.password)
        #     raise ValidationError('Salasanan on virheellinen!')
    #
    # def validate_password(self,password):
    #     u = Users.query.filter_by(email=email.data).first()
    #     if u.password != password:
    #         raise ValidationError('Password is invalid!')



    class Meta:
        csrf = False
