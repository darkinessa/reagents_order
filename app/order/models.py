from app import db
from datetime import datetime
from app.order.constants import STATUS

class ItemInOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_published = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
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
    reagent_status = db.Column(db.String, index=True, default='черновик')

    def __repr__(self):
        return '<ItemInOrder {}>'.format(self.id)
