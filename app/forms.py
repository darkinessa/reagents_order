from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField,  StringField, SubmitField, TextAreaField
from wtforms import Form, IntegerField, SelectField, TextField, FieldList, FormField, SubmitField
from collections import namedtuple
from wtforms.validators import DataRequired
from wtforms import validators




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
    catalogue_number = StringField('Каталожный номер или артикул')
    url_reagent = StringField('Введите ссылку') 
    
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





