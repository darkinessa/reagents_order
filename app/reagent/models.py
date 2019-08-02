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


# class Vendor(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     vendor_id =
#     vendor = db.Column(db.String, index=True)
#     vendor_email = db.Column(db.String, index=True)
#     vendor_contacts = db.Column(db.String, index=True)
#     vendor_site = db.Column(db.String, index=True)
#     vendor_comments = db.Column(db.String)
#
#     def __repr__(self):
#         return '<Vendor {}>'.format(self.vendor_name)