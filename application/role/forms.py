from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import ValidationError, DataRequired
from application.role.models import Role



class RoleForm(FlaskForm):

    role = StringField('Role',validators=[DataRequired("Role is mandatory!")])

    class Meta:
        csrf = False
