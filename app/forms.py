from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField,  StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')

# class LoginForm(FlaskForm):
#     username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
#     password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
#     submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})