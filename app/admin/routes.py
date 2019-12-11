from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from app import app, db
from app.admin.constants import SUPER_ADMIN_EMAILS, STATUS_ACTIONS
from app.admin.decorators import super_admin_required, admin_required
from app.admin.forms import StatusAddForm, StatusDeleteForm
from app.auth.models import User
from app.order.constants import AIM, URGENCY, format_const
from app.order.models import ItemInOrder, Status, Order


@app.route('/start_settings', methods=['GET', 'POST'])
@login_required
@super_admin_required
def start_settings():
    status_table = Status.query.all()
    users = User.query.limit(3).all()
    form1 = StatusAddForm()
    form2 = StatusDeleteForm()
    print(current_user.admin)

    if form1.validate_on_submit():
        if not status_table:
            if current_user.email not in SUPER_ADMIN_EMAILS:
                flash('У вас нет прав доступа вностить изменения в базу данных')
                return redirect(url_for('start_settings'))

            else:
                for status in STATUS_ACTIONS:
                    add_status = Status(name=status[1], action=status[2], flashes=status[3], status=status[4])
                    db.session.add(add_status)
                    db.session.commit()
                flash('Таблица Статусы в базе данных обновлена')
                return redirect(url_for('start_settings'))

    if form2.validate_on_submit():
        if current_user.email not in SUPER_ADMIN_EMAILS:
            flash('У вас нет прав доступа вностить изменения в базу данных')
            return redirect(url_for('start_settings'))
        elif status_table:
            db.session.query(Status).delete(synchronize_session='evaluate')
            db.session.commit()
            flash('Таблица Статусы в базе данных очищена')
            return redirect(url_for('start_settings'))

    return render_template('start_settings.html', status=status_table, form1=form1, form2=form2, users=users)


@app.route('/manage_users', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_users():
    users = User.query.order_by(User.registration_date.desc()).all()

    form_checks = request.form.getlist('checks')

    if '_active' in request.form:
        for item_check in form_checks:
            check_id = int(item_check)
            user = User.query.get(check_id)
            user.role = '2'
            db.session.commit()
            flash(f'Пользователь {user.name} активирован')
        return redirect(url_for('manage_users'))

    if '_active_new' in request.form:

        users = User.query.filter_by(role='1').all()
        for user in users:
            user.role = '2'
            db.session.commit()
            flash(f'Пользователь {user.name} активирован')
        return redirect(url_for('manage_users'))

    if '_deactive' in request.form:

        for item_check in form_checks:
            check_id = int(item_check)
            user = User.query.get(check_id)
            user.role = '3'

            db.session.commit()
            flash(f'Пользователь {user.name} деактивирован')
        return redirect(url_for('manage_users'))

    if '_admin' in request.form:
        for item_check in form_checks:
            check_id = int(item_check)
            user = User.query.get(check_id)
            if user.role != 2:
                flash(
                    'Вы не можете назначить Администратором неактивного пользователя, сначала активируйте его учетгую запись')
                return redirect(url_for('manage_users'))
            user.admin = True
            db.session.commit()
            flash(f'Пользователь {user.name} назначен администратором')
        return redirect(url_for('manage_users'))

    if '_user' in request.form:

        for item_check in form_checks:
            check_id = int(item_check)
            user = User.query.get(check_id)
            user.admin = False

            db.session.commit()
            flash(f"Администратор {user.name} понижен до пользователя")
        return redirect(url_for('manage_users'))

    if '_ban_user' in request.form:

        for item_check in form_checks:
            check_id = int(item_check)
            user = User.query.get(check_id)
            user.role = False

            db.session.commit()
            flash(f"Пользователь {user.name} забанен")
        return redirect(url_for('manage_users'))

    if '_del_user' in request.form:
        # order = ItemInOrder.query.all()

        for item_check in form_checks:
            check_id = int(item_check)
            user = User.query.get(check_id)
            if not current_user.email or current_user.email not in SUPER_ADMIN_EMAILS:
                flash('У вас нет доступа на удаление пользователей')
                return redirect(url_for('manage_users'))
            if user.active is True:
                flash('Вы не можете удалить активного пользователя')
                return redirect(url_for('manage_users'))
            # for item in order:
            #     if item.author == user:
            #         flash('автор')
            #         return redirect(url_for('manage_users'))
            db.session.delete(user)
            db.session.commit()
            flash(f'Пользователь {user.name} удален')

        return redirect(url_for('manage_users'))
    return render_template('manage_users.html', users=users)


@app.route('/admin')
@login_required
@admin_required
def admin():
    items = ItemInOrder.query.all()

    for item in items:
        item.aim_pretty = format_const(item.reagent_aim, AIM)
        item.urgency_pretty = format_const(item.urgency, URGENCY)

    return render_template('admin.html', admin=admin, items=items)


@app.route('/my_items')
@login_required
def my_items():
    items = ItemInOrder.query.filter_by(user_id=current_user.id).filter_by(item_status_id='1').all()
    url = request.endpoint
    for item in items:
        item.aim_pretty = format_const(item.reagent_aim, AIM)
        item.urgency_pretty = format_const(item.urgency, URGENCY)
    return render_template('/items/my_items.html', user=current_user, items=items, url=url)


@app.route('/all_items')
@admin_required
def all_items():
    items = ItemInOrder.query.order_by(ItemInOrder.order_published.desc()).all()
    url = request.endpoint
    for item in items:
        item.aim_pretty = format_const(item.reagent_aim, AIM)
        item.urgency_pretty = format_const(item.urgency, URGENCY)
    return render_template('/items/all_items.html', admin=admin, items=items, url=url)


@app.route('/new_items')
@login_required
@admin_required
def new_items():
    items = ItemInOrder.query.filter_by(item_status_id='2').order_by(ItemInOrder.order_published.desc()).all()
    url = request.endpoint

    for item in items:
        item.aim_pretty = format_const(item.reagent_aim, AIM)
        item.urgency_pretty = format_const(item.urgency, URGENCY)

    return render_template('items/new_items.html', admin=admin, items=items, url=url)


@app.route('/handling_items')
@login_required
@admin_required
def handling_items():
    items = ItemInOrder.query.filter_by(item_status_id='3').order_by(ItemInOrder.vendor_name).all()
    url = request.endpoint

    for item in items:
        item.aim_pretty = format_const(item.reagent_aim, AIM)
        item.urgency_pretty = format_const(item.urgency, URGENCY)

    return render_template('items/handling_items.html', admin=admin, items=items, url=url)


@app.route('/declined_items')
@login_required
@admin_required
def declined_items():
    items = ItemInOrder.query.filter_by(item_status_id='8').all()
    url = request.endpoint

    for item in items:
        item.aim_pretty = format_const(item.reagent_aim, AIM)
        item.urgency_pretty = format_const(item.urgency, URGENCY)

    return render_template('items/declined_items.html', admin=admin, items=items, url=url)


@app.route('/suspended_items')
@login_required
@admin_required
def suspended_items():
    items = ItemInOrder.query.filter_by(item_status_id='9').all()
    url = request.endpoint

    for item in items:
        item.aim_pretty = format_const(item.reagent_aim, AIM)
        item.urgency_pretty = format_const(item.urgency, URGENCY)

    return render_template('items/suspended_items.html', admin=admin, items=items, url=url)


@app.route('/deleted_items')
@login_required
@admin_required
def deleted_items():
    items = ItemInOrder.query.filter_by(item_status_id='10').all()
    url = request.endpoint

    for item in items:
        item.aim_pretty = format_const(item.reagent_aim, AIM)
        item.urgency_pretty = format_const(item.urgency, URGENCY)

    return render_template('items/deleted_items.html', admin=admin, items=items, url=url)


@app.route('/formed_orders')
@login_required
@admin_required
def formed_orders():
    # html -> view -> bl -> dl
    # html - form(action = ...)
    # view - @get created_orders
    # bl - orders_manager.get_orders_list
    # dl - get all orders -> Order.query.all()
    # bl - Order += OrderDTO.items_count = ItemInOrder.query.filter_by(reagent_in_order_id=id).count() !empty
    # view - OrderDTO + user_manager.user_info
    # html - OrderViewModel

    # orders = Order.query.filter_by(order_status_id='4')
    orders = Order.query.filter_by(order_status_id='4').all()
    url = request.endpoint

    for order in orders:
        id = order.id
        order.items_count = ItemInOrder.query.filter_by(reagent_in_order_id=id).count()

    return render_template('orders/formed_orders.html', admin=admin, orders=orders, url=url)


@app.route('/pass_orders')
@login_required
@admin_required
def pass_orders():
    orders = Order.query.filter_by(order_status_id='5').all()
    url = request.endpoint
    for order in orders:
        id = order.id
        order.items_count = ItemInOrder.query.filter_by(reagent_in_order_id=id).count()

    return render_template('orders/pass_orders.html', admin=admin, orders=orders, url=url)


@app.route('/wait_orders')
@login_required
@admin_required
def wait_orders():
    orders = Order.query.filter_by(order_status_id='6').all()
    url = request.endpoint
    for order in orders:
        id = order.id
        order.items_count = ItemInOrder.query.filter_by(reagent_in_order_id=id).count()

    return render_template('orders/wait_orders.html', admin=admin, orders=orders, url=url)


@app.route('/received_orders')
@login_required
@admin_required
def received_orders():
    orders = Order.query.filter_by(order_status_id='7').all()
    url = request.endpoint
    for order in orders:
        id = order.id
        order.items_count = ItemInOrder.query.filter_by(reagent_in_order_id=id).count()

    return render_template('orders/received_orders.html', admin=admin, orders=orders, url=url)


@app.route('/declined_orders')
@login_required
@admin_required
def declined_orders():
    orders = Order.query.filter_by(order_status_id='8').all()
    url = request.endpoint
    for order in orders:
        id = order.id
        order.items_count = ItemInOrder.query.filter_by(reagent_in_order_id=id).count()

    return render_template('orders/declined_orders.html', admin=admin, orders=orders, url=url)


@app.route('/suspended_orders')
@login_required
@admin_required
def suspended_orders():
    orders = Order.query.filter_by(order_status_id='9').all()
    url = request.endpoint
    for order in orders:
        id = order.id
        order.items_count = ItemInOrder.query.filter_by(reagent_in_order_id=id).count()

    return render_template('orders/suspended_orders.html', admin=admin, orders=orders, url=url)


@app.route('/deleted_orders')
@login_required
@admin_required
def deleted_orders():
    orders = Order.query.filter_by(order_status_id='10').all()
    url = request.endpoint
    for order in orders:
        id = order.id
        order.items_count = ItemInOrder.query.filter_by(reagent_in_order_id=id).count()

    return render_template('orders/deleted_orders.html', admin=admin, orders=orders, url=url)


@app.route('/all_orders')
@login_required
@admin_required
def all_orders():
    orders = Order.query.all()
    url = request.endpoint
    for order in orders:
        id = order.id
        order.items_count = ItemInOrder.query.filter_by(reagent_in_order_id=id).count()

    return render_template('orders/all_orders.html', admin=admin, orders=orders, url=url)

#
# @app.route('/delete_order', methods=['GET', 'POST'])
# @admin_required
# def delete_order():
#     pass


#AttributeError