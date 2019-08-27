from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, NumberRange
from app.order.constants import URGENCY, AIM


class ReagentOrderForm(FlaskForm):

    reagent_name = TextAreaField('* Название реактива', validators=[DataRequired()])
    reagent_description = TextAreaField('Описание или техническое задание')

    package = StringField('* Фасовка, например: 500 грамм, 10 шт/уп, 100 мкг и т.п.', validators=[DataRequired()])
    package_unit = StringField('Единица измерения, например: шт, уп, набор и т.п.', validators=[DataRequired()])

    reagent_count = IntegerField('* Количество',
                                 validators=[DataRequired(message="Дай"), NumberRange(min=1, message='Минимальное количество 1')])

    vendor_name = StringField('* Название производителя', validators=[DataRequired()])

    replacement = BooleanField('Возможна замена')

    catalogue_number = StringField('Каталожный номер или артикул')

    url_reagent = StringField('Ссылка на страницу реактива на сайте производителя')

    urgency = SelectField('Срочность заказа (стратегический означает, что можно заказать в течение полугода-года', coerce=int,
                          choices=URGENCY)
    reagent_aim = SelectField('Выберите или введите цель заказа реактива для служебной записки', coerce=int, choices=AIM)

    author_comments = TextAreaField('Комментарий к реактиву')

    submit = SubmitField('Добавить реактив в Заказ', render_kw={"class": "form-check-label"})
