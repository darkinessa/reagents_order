from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField,  StringField, SubmitField, TextAreaField
from wtforms import Form, IntegerField, SelectField, TextField, FieldList, FormField, SubmitField
from collections import namedtuple
from wtforms.validators import DataRequired
from wtforms import validators
from app.models import Reagent

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')



class ReagentForm(FlaskForm):
    reagent_name = StringField('*Название реактива', validators=[DataRequired()])
    reagent_count = IntegerField('*Количество',
                          [validators.Required(), validators.NumberRange(min=1)])
    vendor_name = SelectField('Производитель',
                            choices=[
                                (1, 'Sigma'),
                                (2, 'ThermoFisher'),
                                (3, 'Евроген'),
                                (4, 'Панэко'),
                                (5, 'Millipore'),
                                (6, 'Abcam'),
                                (7, 'Tocris'),
                                (8, 'Свой вариант') 
                            ])
                            #тут нужно модифицировать код, чтобы была возможность
                                                   #вводить свой вариант
    reagent_catalog = StringField('Каталожный номер или артикул')
    url_reagent = StringField('Введите ссылку') 
    #не могу понять, как сделать, чтобы ссылка была ссылкой
    package = StringField('*Фасовка, например, 500 грамм или 15 шт/уп')
    reagent_unit = StringField('Введите единицу измерения, например: шт, уп, набор и т.п.')
    reagent_comment = TextAreaField('Введите комментарий к заказу реактива, если необходимо')
    urgency = SelectField('Срочность заказа (стратегический означает, что можно заказать в течение полугода-года',
                            choices=[
                                (1, 'Срочный'),
                                (2, 'Стратегический'),
                            ])
    reagent_aim = SelectField('Выберите или введите цель заказа реактива для служебной записки',
                            choices=[
                                (1, 'для электрофизиологических работ'),
                                (2, 'для молекулярно-биологических работ'),
                                (3, 'для экспериментов с поведением'),
                                (4, 'для иммуноцитохимических / иммуногистохимических исследований'),
                                (5, 'Cвой вариант')
                            ])
    submit = SubmitField('Добавить реактив в Заказ', render_kw={"class": "form-check-label"})








# OrderEntry = namedtuple('OrderEntry', ['quantity', 'producetype'])
# Order = namedtuple('Order', ['name', 'order_entries'])

# class OrderEntryForm(Form):
#   quantity = IntegerField('Quantity',
#                           [validators.Required(), validators.NumberRange(min=1)])
#   # we will be dynamically adding choices
#   producetype = SelectField('Produce',
#                             [validators.Required()],
#                             choices=[
#                                 (1, 'carrots'),
#                                 (2, 'turnips'),
#                             ])

# class OrderForm(Form):
#   name = TextField('Crop', [validators.Length(min=3, max=60)])
#   order_entries = FieldList(FormField(OrderEntryForm))

# # Test Print of just the OrderEntryForm
# o_form = OrderEntryForm()
# print o_form.producetype()

# # Create a test order
# order_entry_1 = OrderEntry(4, 1)
# order_entry_2 = OrderEntry(2, 2)

# order = Order('My First Order', [order_entry_1, order_entry_2])

# order_form = OrderForm(obj=order)

# print order_form.name
# print order_form.order_entries    



