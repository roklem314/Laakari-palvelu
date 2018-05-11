from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField,SubmitField,RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from application.registration.models import Accounts
# import bcrypt


class RegistrationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired('Name is mandatory!')])
    address = StringField('Address', validators=[DataRequired('Address is mandatory!')])
    postal_code = StringField('Postalcode',validators=[DataRequired('Postalcode is mandatory!')])
    post_office = StringField('Postoffice',validators=[DataRequired('Postoffice is mandatory!')])
    email = StringField('Email', validators=[DataRequired('Email is mandatory!'), Email("Please check your email!")])
    password = PasswordField('Password',validators=[DataRequired('Password is mandatory!')])
    password2 = PasswordField('Password again', validators=[DataRequired('Please give password again!'),EqualTo("password")])

    def validate_email(self, email):
        u = Accounts.query.filter_by(email=email.data).first()
        if u is not None:
            raise ValidationError('Email address is already in use!')

    def validate_password(self,password):
        if len(password.data) < 8:
            raise ValidationError('Password must be at least 8 characters!')

    class Meta:
        csrf = False

class ModifyForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired('Name is mandatory!')])
    email = StringField('Email', validators=[DataRequired('Email is mandatory!'), Email("Please check your email!")])
    password = PasswordField('Password',validators=[DataRequired('Password is mandatory!')])
    password2 = PasswordField('Password again', validators=[DataRequired('Please give password again!'),EqualTo("password")])

    def validate_email_password(self, email):
        u = Accounts.query.filter_by(email=email.data).first()
        if u is not None:
            if u.email != current_user.email:
                raise ValidationError('Email address is already in use!')

    def validate_password(self,password):
        u = Accounts.query.filter_by(email=current_user.email).first()
        # if  0 == u.check_password(password.data):
        # time.sleep(10)
        # if not bcrypt.checkpw(password.data.encode("utf-8"), u.password):
        if len(password.data) < 8:
            raise ValidationError('Password must be at least 8 characters!')
        if (u.password != password.data):
            raise ValidationError('Password is invalid!')


    class Meta:
        csrf = False

class DeleteForm(FlaskForm):
    password = PasswordField('Confirm by entering a password',validators=[DataRequired("Password is mandatory!")])
    password2 = PasswordField('Password again', validators=[DataRequired('Please give password again!'),EqualTo("password")])

    def validate_password(self,password):
        u = Accounts.query.filter_by(email=current_user.email).first()
        # if  0 == u.check_password(password.data):
        # time.sleep(10)
        # if not bcrypt.checkpw(password.data.encode("utf-8"), u.password):
        if not (u.password == password.data):
            raise ValidationError('Password is invalid!')


    class Meta:
        csrf = False

class DoctorRegistrationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired('Name is mandatory!')])
    address = StringField('Address', validators=[DataRequired('Address is mandatory!')])
    postal_code = StringField('Postalcode',validators=[DataRequired('Postalcode is mandatory!')])
    post_office = StringField('Postoffice',validators=[DataRequired('Postoffice is mandatory!')])
    email = StringField('Email', validators=[DataRequired('Email is mandatory!'), Email("Please check your email!")])

    def validate_email(self, email):
        u = Accounts.query.filter_by(email=email.data).first()
        if u is not None:
            raise ValidationError('Email address is already in use!')


    class Meta:
        csrf = False
