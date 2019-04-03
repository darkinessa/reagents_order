from app import app, db
from app.forms import LoginForm, ReagentForm
from flask import flash, redirect, render_template, url_for
from flask_wtf import FlaskForm
from app.models import Reagent

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход в личный кабинет', form=form)


# @app.route('/reagent_get', methods=['GET', 'POST'])
# def submit():
#     form = ReagentForm()
#     # if form.validate_on_submit():
#     #     return redirect('/index')
#     return render_template('reagent_get.html', form=form)


@app.route('/reagent_get', methods=['GET', 'POST'])
def submit():
    form = ReagentForm()
    if form.validate_on_submit():
        reagent = Reagent(reagent_name = form.reagent_name.data, 
                vendor_name = form.vendor_name.data, 
                reagent_catalog = form.reagent_catalog.data,
                url_reagent = form.url_reagent.data)
        db.session.add(reagent)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('reagent_get.html', title='Заказ нового реактив', form=form)