from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    name = db.Column(db.String(192), index=True, unique=True)
    phone_number = db.Column(db.String(32))
    supervisor = db.Column(db.String(192), index=True)
    position = db.Column(db.String(128), index=True)
    laboratory = db.Column(db.String(192), index=True)
    role = db.Column(db.String(16), index=True)
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Order', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Order {}>'.format(self.body)
