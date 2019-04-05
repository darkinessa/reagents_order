from app import db


class Reagent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reagent_name = db.Column(db.String, index=True, nullable=False)
    package = db.Column(db.String, index=True)
    package_unit = db.Column(db.String, index=True)
    vendor_name = db.Column(db.String, index=True, nullable=False)
    catalogue_number = db.Column(db.String, index=True)
    url_reagent = db.Column(db.String, nullable=True)
    reagent_comments = db.Column(db.String)
    # reagents_in_item = db.relationship('ItemInOrder', lazy='dynamic')

    def __repr__(self):
        return '<Reagent {}>'.format(self.reagent_name)


class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller = db.Column(db.String, index=True)
    seller_email = db.Column(db.String, index=True)
    seller_contacts = db.Column(db.String, index=True)
    seller_comments = db.Column(db.String)

    def __repr__(self):
        return '<Seller {}>'.format(self.seller_name)