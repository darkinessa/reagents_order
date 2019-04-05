from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    name = db.Column(db.String(192), index=True, unique=True)
    phone_number = db.Column(db.String(64))
    supervisor = db.Column(db.String(192), index=True)
    position = db.Column(db.String(128), index=True)
    laboratory = db.Column(db.String(192), index=True)
    role = db.Column(db.String(16), index=True)
    password_hash = db.Column(db.String(128))
#orders = db.relationship('Order', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
