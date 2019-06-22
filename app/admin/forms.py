from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired, ValidationError
from app.auth.models import User
from app.admin.constants import SUPER_ADMIN_EMAILS
from app.order.models import Status


class StatusAddForm(FlaskForm):
    fill_table = SubmitField('Заполнить таблицу по умолчанию', render_kw={"class": "btn btn-info"})


    def validate_admin(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user not in SUPER_ADMIN_EMAILS:
            raise ValidationError('У вас нет прав доступа вностить изменения в базу данных')


class StatusDeleteForm(FlaskForm):
    delete_table = SubmitField('Очистить базу данных')