from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL

from app.reagent.models import Reagent



class ReagentForm(FlaskForm):

    reagent_name = StringField('Название реактива', validators=[DataRequired()])

    package = StringField('Фасовка, например: 500 грамм, 10 шт/уп, 100 мкг, 200 мг и т.п.', validators=[DataRequired()])
    package_unit = StringField('Единица измерения, например: шт, уп, набор и т.п.', validators=[DataRequired()])

    vendor_name = StringField('Название производителя', validators=[DataRequired()])

    catalogue_number = StringField('Каталожный номер или артикул')

    url_reagent = StringField('Ссылка на страницу реактива на сайте производителя')

    reagent_comments = StringField('Комментарий к реактиву')

    submit = SubmitField('Добавить реактив в Базу', render_kw={"class": "form-check-label"})

