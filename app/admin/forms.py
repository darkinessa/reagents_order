from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired, ValidationError
from app.auth.models import User
from app.admin.constants import SUPER_ADMIN_EMAILS
from app.order.models import Status


class StatusAddForm(FlaskForm):
    fill_table = SubmitField('Заполнить таблицу по умолчанию',
            render_kw={"onclick": "return confirm('Вы действительно хотите обновить таблицу Статусы в базе данных?');"})


class StatusDeleteForm(FlaskForm):

    delete_table = SubmitField('Очистить базу данных',
            render_kw={"onclick": "return confirm('Вы действительно хотите очистить таблицу Статусы в базе данных?');"})
