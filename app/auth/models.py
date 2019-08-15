from datetime import date, datetime

from flask_login import UserMixin
from sqlalchemy.sql import expression
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column('email', db.String(128), index=True, unique=True)
    email_confirmed_at = date.today()
    surname = db.Column(db.String(192), index=True)
    name = db.Column(db.String(192), index=True)
    phone_number = db.Column(db.String(64))
    supervisor = db.Column(db.String(192), index=True)
    position = db.Column(db.String(128), index=True)
    laboratory = db.Column(db.String(192), index=True)
    password = db.Column('password_hash', db.String(128))
    admin = db.Column(db.Boolean, default=False, nullable=False, index=True)
    role = db.Column(db.Integer, default=1, nullable=False, index=True)
    registration_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    item_in_orders = db.relationship('ItemInOrder', backref='author', lazy='dynamic')


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '{}'.format(self.name)


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
