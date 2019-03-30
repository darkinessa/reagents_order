from app import db
from datetime import datetime

#User - из репозитория Иры
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


class Reagent(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String, nullable=False) #обязательное поле
        vendor_name = db.Column(db.String, nullable=True)
        reagent_catalog = db.Column(db.String, nullable=True, )
        url_reagent = db.Column(db.String, nullable=True)
        reagents_in_item = db.relationship('ItemInOrder', lazy='dynamic')
        
        def __repr__(self):
            return '<Reagent {}>'.format(self.title)


class Order(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        order_published = db.Column(db.DateTime, default=datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        order_status = db.Column(db.String, nullable=False) 
        #тут будет статус "Новый заказ", "Черновик заказа", "Отправленные заказы", "Архив"
        def __repr__(self):
            return '<Order {}>'.format(self.order_date)


class ItemInOrder(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        reagent_id = db.Column(db.Integer, db.ForeignKey('reagent.id'))
        package = db.Column(db.String, nullable=True)
        reagent_count = db.Column(db.Integer, nullable=False) #обязательное поле
        reagent_comment = db.Column(db.String, nullable=True)
        urgency = db.Column(db.String, nullable=True)
        reagent_aim = db.Column(db.String, nullable=True)
        order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
        item_status = db.Column(db.String, nullable=False) 
        #Отправлено поставщику
        # Ожидается поставка
        # Пришла поставка

        def __repr__(self):
            return '<ItemInOrder {}>'.format(self.id)


# - еще может быть будет класс Поставщик (Seller), но позже
# reagent_sort = db.Column(db.String, nullable=True) - это про вид реактива и код ОКДП, с ним решим позже

