from datetime import date

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from app.auth.constants import ADMIN


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column('email', db.String(128), index=True, unique=True)
    email_confirmed_at = date.today()
    name = db.Column(db.String(192), index=True)
    phone_number = db.Column(db.String(64))
    supervisor = db.Column(db.String(192), index=True)
    position = db.Column(db.String(128), index=True)
    laboratory = db.Column(db.String(192), index=True)
    password = db.Column('password_hash', db.String(128))
    is_admin = db.Column(db.Boolean(), default=False)
    is_active = db.Column(db.Boolean(), default=False)
    item_in_orders = db.relationship('ItemInOrder', backref='author', lazy='dynamic')


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '{}'.format(self.name)

    def is_admin(self):
        return self.is_admin is True

    def is_active(self):
        return self.is_active is True


@login.user_loader
def load_user(id):
    return User.query.get(id)


# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(28), unique=True)
#
#     def __repr__(self):
#         return '{}'.format(self.name)
#
#     def is_admin(self):
#         return self.name == ADMIN
#
#
# class UserRoles(db.Model):
#     __tablename__ = 'user_roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
#
#     def __repr__(self):
#         return '{}'.format(self.role_id)
