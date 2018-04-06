from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField,SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from application.registration.models import Users
import bcrypt


class RegistrationForm(FlaskForm):
    name = StringField('Nimi',validators=[DataRequired("Nimi on pakollinnen!")])
    address = StringField('Osoite', validators=[DataRequired("Osoite on pakollinnen!")])
    # social_sec_num = StringField('Identity number',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired("Sähköposti on pakollinnen!"), Email("Tarkista sähköposti osoite!")])
    password = PasswordField('Salasana',validators=[DataRequired("Salasana on pakollinen!")])
    password2 = PasswordField('Salasana', validators=[DataRequired("Anna salasana uudelleen!"),EqualTo("password")])

    def validate_email(self, email):
        u = Users.query.filter_by(email=email.data).first()
        if u is not None:
            raise ValidationError('Sähköposti osoite on jo käytössä!.')

    def validate_password(self,password):

        if len(password.data) < 8:
            raise ValidationError('Salasanan täytyy olla vähintään 8 merkkiä!')

    class Meta:
        csrf = False

class ModifyForm(FlaskForm):
    name = StringField('Nimi',validators=[DataRequired("Nimi on pakollinnen!")])
    address = StringField('Osoite', validators=[DataRequired("Osoite on pakollinnen!")])
    # social_sec_num = StringField('Identity number',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired("Sähköposti on pakollinnen!"), Email("Tarkista sähköposti osoite!")])
    password = PasswordField('Salasana',validators=[DataRequired("Salasana on pakollinen!")])
    password2 = PasswordField('Toista salasana', validators=[DataRequired("Anna salasana uudelleen!"),EqualTo("password")])

    def validate_email(self, email):
        u = Users.query.filter_by(email=email.data).first()
        if u is not None:
            if u.email != current_user.email:
                raise ValidationError('Sähköposti osoite on jo käytössä!.')

    def validate_password(self,password):

        if len(password.data) < 8:
            raise ValidationError('Salasanan täytyy olla vähintään 8 merkkiä!')

    class Meta:
        csrf = False

class DeleteForm(FlaskForm):
    password = PasswordField('Salasana',validators=[DataRequired("Salasana on pakollinen!")])
    password2 = PasswordField('Toista salasana', validators=[DataRequired("Anna salasana uudelleen!"),EqualTo("password")])

    def validate_password(self,password):
        u = Users.query.filter_by(email=current_user.email).first()
        # if  0 == u.check_password(password.data):
        if not bcrypt.checkpw(password.data.encode("utf-8"), u.password):
            raise ValidationError('Salasanan on virheellinen!')


    class Meta:
        csrf = False
