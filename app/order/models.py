from app import db
from datetime import datetime
from app.order.constants import STATUS


class ItemInOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_published = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reagent_name = db.Column(db.String, index=True, nullable=False)
    package = db.Column(db.String, index=True)
    package_unit = db.Column(db.String, index=True)
    reagent_count = db.Column(db.Integer)
    vendor_name = db.Column(db.String, index=True, nullable=False)
    catalogue_number = db.Column(db.String, index=True)
    url_reagent = db.Column(db.String, nullable=True)
    urgency = db.Column(db.String, index=True)
    reagent_aim = db.Column(db.String, index=True)
    reagent_comments = db.Column(db.String)
    item_status = db.relationship('Status', secondary='item_statuses')

    def __repr__(self):
        return '<ItemInOrder {}>'.format(self.id)


class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)

    def __repr__(self):
        return '{}'.format(self.name)


class ItemStatuses(db.Model):
    __tablename__ = 'item_statuses'
    id = db.Column(db.Integer(), primary_key=True)
    item_id = db.Column(db.Integer(), db.ForeignKey('item_in_order.id', ondelete='CASCADE'))
    status_id = db.Column(db.Integer(), db.ForeignKey('status.id', ondelete='CASCADE'))

    def __repr__(self):
        return '{}'.format(self.status_id)


