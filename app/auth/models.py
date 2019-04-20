from datetime import date

from app import app, db, login
from flask_user import UserMixin
from flask_user import UserManager
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth import constants as USER


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email_str = db.Column('email', db.String(128), index=True, unique=True)
    email_confirmed_at = date.today()
    name = db.Column(db.String(192), index=True)
    phone_number = db.Column(db.String(64))
    supervisor = db.Column(db.String(192), index=True)
    position = db.Column(db.String(128), index=True)
    laboratory = db.Column(db.String(192), index=True)
    password = db.Column('password_hash', db.String(128))
    roles = db.relationship('Role', secondary='user_roles')
    item_in_orders = db.relationship('ItemInOrder', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def email(self):
        return self.email_str   # on user.email: return user.email_address

    # define email setter
    @email.setter
    def email(self, value):
        self.email_str = value  # on user.email='xyz': set user.email_

    def __repr__(self):
        return '{}'.format(self.name)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(28), unique=True)

    def __repr__(self):
        return '{}'.format(self.name)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    def __repr__(self):
        return '{}'.format(self.name)


user_manager = UserManager(app, db, User)
user_manager.login_manager = login