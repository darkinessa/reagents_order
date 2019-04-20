from flask import render_template
from flask_login import login_required
from flask_user import roles_required

from app import app
from app.order.constants import AIM, URGENCY
from app.order.models import ItemInOrder


@app.route('/admin')
@login_required
@roles_required('Admin')
def admin():
    items = ItemInOrder.query.all()
    for item in items:
        item.aim_pretty = format_const(item.reagent_aim, AIM)
        item.urgency_pretty = format_const(item.urgency, URGENCY)

    return render_template('admin.html', admin=admin, items=items)


def format_const(key, constants_list):
    for value in constants_list:
        if key in value:
            return value[1]


