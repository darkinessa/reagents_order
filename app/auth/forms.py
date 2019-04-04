from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired, ValidationError
from app.auth.models import User


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={"class": "form_control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form_control"})
    remember_me = BooleanField('Запомнить', render_kw={"class": "form-check-label"})
    submit = SubmitField('Войти', render_kw={"class": "form-check-label"})


class RegistrationForm(FlaskForm):
    username = StringField('Введите Ваш логин', validators=[DataRequired()])
    email = StringField('Введите Ваш email', validators=[DataRequired(), Email()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите введеный пароль', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Ведите имя и фамилию', validators=[DataRequired()])
    phone_number = StringField('Введите свой контакнтый телефон', validators=[DataRequired()])
    position = StringField('Должность')
    laboratory = StringField('Лаборатория')
    supervisor = StringField('Научный руководитель')
    submit = SubmitField('Зарегистрироваться', render_kw={"class": "form-check-label"})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Данный логин занят, используйте другой')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Данный email уже используется, введите другой')
