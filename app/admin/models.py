# from app import db, login
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
# from app.auth import constants as USER
#
#
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(128), index=True, unique=True)
#     name = db.Column(db.String(192), index=True)
#     phone_number = db.Column(db.String(64))
#     supervisor = db.Column(db.String(192), index=True)
#     position = db.Column(db.String(128), index=True)
#     laboratory = db.Column(db.String(192), index=True)
#     password_hash = db.Column(db.String(128))
#     roles = db.relationship('Role', secondary='user_roles')
#     item_in_orders = db.relationship('ItemInOrder', backref='author', lazy='dynamic')
#
#     def __repr__(self):
#         return '{}'.format(self.name)
#
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
#
# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))
#
# c