from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField,SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from application.role.models import Role



class RoleForm(FlaskForm):

    role = StringField('Rooli',validators=[DataRequired("Osoite on pakollinen")])

    class Meta:
        csrf = False
