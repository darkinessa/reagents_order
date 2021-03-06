from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.auth.forms import LoginForm, RegistrationForm
from app.auth.models import User
from app.order.constants import AIM, URGENCY, format_const
from app.order.models import ItemInOrder, Status


# @app.template_filter('is_active')
# def is_active(func):
#     if current_user.is_authenticated:
#         if current_user.role == 2:
#             return True
#         return False
#     return False


@app.route('/')
@app.route('/index')
# @login_required
def index():
    return render_template('index.html', title='Home', items=ItemInOrder.query.all())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин или пароль')
            return redirect(url_for('login'))
        if user.role == 0:
            abort(401)

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход в личный кабинет', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    name=form.name.data, surname=form.surname.data, phone_number=form.phone_number.data,
                    supervisor=form.supervisor.data, position=form.position.data, laboratory=form.laboratory.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/user')
@app.route('/user/')
@login_required
def user():
    items = ItemInOrder.query.filter_by(user_id=current_user.id).filter_by(item_status_id='1').all()
    url = request.endpoint
    print(url)

    for item in items:
        item.aim_pretty = format_const(item.reagent_aim, AIM)
        item.urgency_pretty = format_const(item.urgency, URGENCY)

    return render_template('user.html', user=current_user, items=items, url=url)
