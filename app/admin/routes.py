from flask import flash, redirect, render_template, request, url_for,  current_app
from flask_login import login_required, login_manager, current_user

from werkzeug.urls import url_parse

from functools import wraps

from app import app
from app.auth.models import User
from app.order.constants import AIM, URGENCY
from app.order.models import ItemInOrder


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
    # users = User.query.all()
    # print(users, len(users))

    for item in items:
        item.aim_pretty = format_const(item.reagent_aim, AIM)
        item.urgency_pretty = format_const(item.urgency, URGENCY)

    return render_template('admin.html', admin=admin, items=items)

