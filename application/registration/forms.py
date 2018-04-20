from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField,SubmitField,RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from application.registration.models import Users
# import bcrypt


class RegistrationForm(FlaskForm):
    name = StringField('Nimi',validators=[DataRequired("Nimi on pakollinnen!")])
    role = StringField('Rooli',validators=[DataRequired("Kenttä on pakollinnen!")])
    # gender = RadioField('Sukupuoli', choices=[('value1','muu'),('value2','nainen'),('value2','mies')],validators=[DataRequired("Valinta on pakollinen!")])
    address = StringField('Osoite', validators=[DataRequired("Osoite on pakollinnen!")])
    postalCode = StringField('Postinumero',validators=[DataRequired("Postinumero on pakollinen")])
    postOffice = StringField('Postitoimipaikka',validators=[DataRequired("Postinumero on pakollinen")])
    email = StringField('Email', validators=[DataRequired("Sähköposti on pakollinnen!"), Email("Tarkista sähköposti osoite!")])
    password = PasswordField('Salasana',validators=[DataRequired("Salasana on pakollinen!")])
    password2 = PasswordField('Salasana', validators=[DataRequired("Anna salasana uudelleen!"),EqualTo("password")])

    def validate_email(self, email):
        u = Users.query.filter_by(email=email.data).first()
        if u is not None:
            raise ValidationError('Sähköposti osoite on jo käytössä!.')
    # def validate_role(self, gender):
    #     if gender is not null:
    #         raise ValidationError('Valinta puuttuu!.')

    def validate_password(self,password):

        if len(password.data) < 8:
            raise ValidationError('Salasanan täytyy olla vähintään 8 merkkiä!')

    class Meta:
        csrf = False

class ModifyForm(FlaskForm):
    name = StringField('Nimi',validators=[DataRequired("Nimi on pakollinnen!")])
    email = StringField('Email', validators=[DataRequired("Sähköposti on pakollinnen!"), Email("Tarkista sähköposti osoite!")])
    password = PasswordField('Salasana',validators=[DataRequired("Salasana on pakollinen!")])
    password2 = PasswordField('Toista salasana', validators=[DataRequired("Anna salasana uudelleen!"),EqualTo("password")])

    def validate_email_password(self, email):
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
        # time.sleep(10)
        # if not bcrypt.checkpw(password.data.encode("utf-8"), u.password):
        if not (u.password == password.data):
            raise ValidationError('Salasanan on virheellinen!')


    class Meta:
        csrf = False
