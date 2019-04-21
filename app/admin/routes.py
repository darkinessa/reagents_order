from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from werkzeug.urls import url_parse

from app import app
from app.order.constants import AIM, URGENCY
from app.order.models import ItemInOrder


@app.route('/admin')
@login_required
def admin():
    if is_admin(admin):
        items = ItemInOrder.query.all()
        for item in items:
            item.aim_pretty = format_const(item.reagent_aim, AIM)
            item.urgency_pretty = format_const(item.urgency, URGENCY)

        return render_template('admin.html', admin=admin, items=items)
    else:
        return redirect(url_for('user'))


def format_const(key, constants_list):
    for value in constants_list:
        if key in value:
            return value[1]


def is_admin(c_u):
    user = current_user
    roles = 'Admin'
    if not user.roles:
        return False
    else:
        if str(user.roles[0]) == roles:
            return True


@app.template_filter('is_admin')
def is_admin(c_u):
    user = current_user
    roles = 'Admin'
    if not user.roles:
        return False
    else:
        if str(user.roles[0]) == roles:
            return True


