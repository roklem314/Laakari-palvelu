from application import db,app
from flask_login import current_user
from application.models import Base
from application.role.forms import RoleForm
from application.role.models import Role
from application.location.models import Location
from sqlalchemy.sql import text


class Users(Base):
    __tablename__ = "account"

    name = db.Column('name', db.String(144), nullable=False)
    email = db.Column('email', db.String(25), unique=True)
    password = db.Column('password', db.String())
    appts = db.relationship("Appointment", backref='account', lazy=True)
    loacation_id= db.Column(db.Integer, db.ForeignKey('location.id'),
                           nullable=True)
    role = db.relationship("user_role",backref = 'account',lazy = True)

    def __init__(self, name,email,password):
        self.name = name
        self.email = email
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    # def role(self):
    #     return role

    @staticmethod
    def roles(email):
        stmt = text("SELECT Role.role FROM account,Role "
                    " WHERE (account.id = Role.id) AND (account.email = :email) ").params(email = email)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({row[0]})

        return response

    # @staticmethod
    # def insert_admin_with_location():
    #     stmt = text("INSERT INTO Role(role) VALUES("ADMIN")")
    #     res = db.engine.execute(stmt)
    #     # stmt = text("INSERT INTO Location(address,postal_code,post_office) VALUES("null","null","","null",1)")
    #     # res = db.engine.execute(stmt)
    #     stmt = text("INSERT INTO Account(name,email,password,appts,location_id,role) VALUES("ADMIN","admin@testi.com","","ADMIN1234",,,1)")
    #     res = db.engine.execute(stmt)



    # def set_password(self, password):
    #     self.password = generate_password_hash(password)
    #
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password, password)
