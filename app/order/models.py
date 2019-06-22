from app import db
from datetime import datetime


class ItemInOrder(db.Model):
    __tablename__ = 'Item_in_order'
    id = db.Column(db.Integer, primary_key=True)
    order_published = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    date_change = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reagent_name = db.Column(db.String(512), index=True, nullable=False)
    package = db.Column(db.String(56), index=True)
    package_unit = db.Column(db.String(42), index=True)
    reagent_count = db.Column(db.Integer)
    vendor_name = db.Column(db.String(256), index=True, nullable=False)
    catalogue_number = db.Column(db.String(56), index=True)
    url_reagent = db.Column(db.String(256), nullable=True)
    urgency = db.Column(db.Integer, index=True)
    reagent_aim = db.Column(db.Integer, index=True)
    reagent_comments = db.Column(db.Text)
    item_status = db.relationship('Status')
    item_status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    item_replace = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<ItemInOrder {}>'.format(self.id)


class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(56), index=True)
    action = db.Column(db.String(14), index=True)
    flashes = db.Column(db.String(128), index=True)

    def __repr__(self):
        return '{}'.format(self.name)
