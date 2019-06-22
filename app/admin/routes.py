from flask import flash, redirect, render_template, request, url_for, current_app
from flask_login import login_required, login_manager, current_user

from werkzeug.urls import url_parse

from functools import wraps

from app import app, db
from app.admin.constants import SUPER_ADMIN_EMAILS, STATUS_ACTIONS
from app.admin.forms import StatusAddForm, StatusDeleteForm
from app.auth.models import User
from app.order.constants import AIM, URGENCY
from app.order.models import ItemInOrder, Status


def super_admin_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        print(current_user)

        if not current_user.email or current_user.email not in SUPER_ADMIN_EMAILS:
            return redirect(url_for('index'))
        return func(*args, **kwargs)

    return wrapped


@app.template_filter('super_admin')
def super_admin(func):
    email_list = ['korolevai@gmail.com', 'irina@koroleva.org', 'nneuro2013@gmail.com']
    if current_user.email not in email_list:
        return False
    return True


def admin_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not current_user.roles or not current_user.roles[0].is_admin():
            return redirect(url_for('index'))
        return func(*args, **kwargs)

    return wrapped


@app.template_filter('is_admin')
def is_admin(func):
    if not current_user.roles or not current_user.roles[0].is_admin():
        return False
    return True


def format_const(key, constants_list):
    for value in constants_list:
        if key in value:
            return value[1]


@app.route('/admin')
@login_required
@admin_required
def admin():
    items = ItemInOrder.query.all()
    users = User.query.all()
    # print(users, len(users))
    #    print(current_user.email)

    for item in items:
        item.aim_pretty = format_const(item.reagent_aim, AIM)

        if item.urgency is 0:
            print('h')
        else:
            print('cao')
        item.urgency_pretty = format_const(item.urgency, URGENCY)
        print(item.urgency_pretty, item.aim_pretty)

    return render_template('admin.html', admin=admin, items=items)


@app.route('/start_settings', methods=['GET', 'POST'])
@login_required
@super_admin_required
def start_settings():
    status_table = Status.query.all()
    form1 = StatusAddForm()
    form2 = StatusDeleteForm()
    print(status_table)

    if form1.validate_on_submit():
        if not status_table:
            for status in STATUS_ACTIONS:
                add_status = Status(name=status[1], action=status[2], flashes=status[3])
                db.session.add(add_status)
                db.session.commit()
            flash('База обновлена')
            return redirect(url_for('start_settings'))

    if form2.validate_on_submit():
        if status_table:
            db.session.query(Status).delete(synchronize_session='evaluate')
            db.session.commit()
            flash('База очищена')
            return redirect(url_for('start_settings'))

    return render_template('start_settings.html', status=status_table, form1=form1, form2=form2)
