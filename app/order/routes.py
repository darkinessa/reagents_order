from datetime import datetime

from six import StringIO, BytesIO
from werkzeug.datastructures import Headers
from werkzeug.urls import url_parse

from app import app, db
from flask import redirect, render_template, url_for, flash, request, send_file

from app.admin.decorators import admin_required
from app.auth.decorators import active_user_required
from app.order.constants import URGENCY, AIM, format_const, REPORT_CHOICE
from app.order.models import ItemInOrder, Status, Order
from app.order.forms import ReagentOrderForm, CreateOrderForm
from flask_login import current_user, login_required


@app.template_filter()
def urgency_format(key):
    for value in URGENCY:
        if key in value:
            return value[1]


@app.template_filter()
def aim_format(key):
    for value in AIM:
        if key in value:
            return value[1]

@app.route('/item', methods=['GET', 'POST'])
@login_required
@active_user_required
def item_add():
    form = ReagentOrderForm()
    print(form.reagent_aim.data, form.reagent_aim.data)

    if form.validate_on_submit():
        reagent = ItemInOrder(author=current_user,
                              reagent_name=form.reagent_name.data, reagent_description=form.reagent_description.data,
                              package=form.package.data,
                              package_unit=form.package_unit.data, vendor_name=form.vendor_name.data,
                              catalogue_number=form.catalogue_number.data, url_reagent=form.url_reagent.data,
                              urgency=int(form.urgency.data), reagent_comments=form.reagent_comments.data,
                              reagent_aim=form.reagent_aim.data, reagent_count=form.reagent_count.data,
                              item_status_id='1')
        db.session.add(reagent)
        db.session.commit()
        flash('Реактив добавлен в Заказ')
        return redirect(url_for('item_add'))

    return render_template('item.html', title='Добавление нового реактива', form=form)


# @app.route('/delete_item/<int:id>', methods=['POST'])
# @login_required
# def delete_item(id):
#     item = ItemInOrder.query.get(id)
#
#     if item.item_status_id != 9:
#         print(item.item_status_id)
#         flash('Вы не можете удалить Реагент, который не помечен "На удаление"')
#         return redirect(url_for('trash'))
#
#     if item is None:
#         flash('Реагент не найден')
#         return redirect(url_for('trash'))
#
#     if current_user != item.author or not current_user.roles[0].is_admin():
#         print(current_user, item.author)
#         flash('У вас нет прав на удаление этого реагента')
#         return redirect(url_for('trash'))
#
#     db.session.delete(item)
#     db.session.commit()
#     flash('Реагент удален')
#     return redirect(url_for('trash'))


@app.route('/delete_trash', methods=['GET', 'POST'])
@login_required
def delete_trash():
    form_checks = request.form.getlist('checks')
    reagents = ItemInOrder.query.filter_by(user_id=current_user.id).filter_by(item_status_id='9').all()
    if 'delete' in request.form:
        for reagent_check in form_checks:
            check_id = int(reagent_check)
            reagent = ItemInOrder.query.get(check_id)
            if reagent.item_status_id != 9:
                print(reagent.item_status_id)
                flash('Вы не можете удалить Реагент, который не помечен "На удаление"')
                return redirect(url_for('delete_trash'))

            if reagent is None:
                flash('Реагент не найден')
                return redirect(url_for('delete_trash'))

            if current_user != reagent.author and not current_user.admin:
                print(current_user, reagent.author)
                flash('У вас нет прав на удаление этого реагента')
                return redirect(url_for('delete_trash'))

            db.session.delete(reagent)
            db.session.commit()
            flash('Реагент удален')
            return redirect(url_for('delete_trash'))

    return render_template('trash.html', title='Корзина', items=reagents)


@app.route('/checked', methods=['GET', 'POST'])
@login_required
def checked(order_id=None, url=None):
    form_checks = request.form.getlist('checks')
    url = request.args.get('url') or request.form.get('url')
    print(url)
    statuses = Status.query.all()
    # print([(s.id, s.name, s.action, s.flashes) for s in statuses])
    for item in statuses:

        action = item.action
        action_id = item.id
        action_flash = item.flashes

        if action in request.form:
            for item_check in form_checks:
                date = datetime.utcnow()
                check_id = int(item_check)
                reagent = ItemInOrder.query.get(check_id)
                reagent.item_status_id = action_id
                reagent.date_change = date
                db.session.commit()
                flash(action_flash)
        elif '_num' in request.form:
            return redirect(url_for('create_order', form_checks=form_checks))

        elif '_append' in request.form:
            id = request.form.get('order_id')
            order = Order.query.filter_by(id=id).first()

            for check in form_checks:
                check_id = int(check)
                reagent = ItemInOrder.query.get(check_id)
                reagent.reagent_in_order_id = id

                reagent.item_status_id = '4'
                db.session.commit()
                flash(f'Реагент { reagent.reagent_name } добавлен в заказ № {order.number}')

            return redirect(url_for('formed_orders', form_checks=form_checks))

    if current_user.admin:
        return redirect(url_for(str(url)))

    else:
        return redirect(url_for('user'))


@app.route('/full_item/<int:id>/', methods=['GET', 'POST'])
@login_required
def full_item(id):
    item = ItemInOrder.query.get(id)

    select_fields = Status.query.all()
    select_urgency = URGENCY
    select_aim = AIM

    date = item.order_published

    strg = f'{item.order_published:%d.%m.%Y}'

    item.aim_pretty = format_const(item.reagent_aim, AIM)
    item.urgency_pretty = format_const(item.urgency, URGENCY)

    if request.method == 'POST':

        if 'copy' in request.form:
            item = item

            reagent = ItemInOrder(author=current_user,
                                  reagent_name=item.reagent_name, reagent_description=item.reagent_description,
                                  package=item.package,
                                  package_unit=item.package_unit, vendor_name=item.vendor_name,
                                  catalogue_number=item.catalogue_number, url_reagent=item.url_reagent,
                                  urgency=item.urgency, reagent_comments=item.reagent_comments,
                                  reagent_aim=item.reagent_aim, reagent_count=item.reagent_count,
                                  item_status_id='1')
            db.session.add(reagent)
            db.session.commit()
            flash('Реактив скопирован')

        if 'edit' in request.form:
            error = None

            item.reagent_name = request.form['reagent_name']
            item.reagent_description = request.form['reagent_description']
            item.package = request.form['package']
            item.package_unit = request.form['package_unit']
            item.vendor_name = request.form['vendor_name']
            item.catalogue_number = request.form['catalogue_number']
            item.url_reagent = request.form['url_reagent']
            item.urgency = request.form['urgency']
            item.reagent_comments = request.form['reagent_comments']
            item.reagent_aim = request.form['reagent_aim']
            item.reagent_count = request.form['reagent_count']
            item.item_status_id = request.form['item_status']
            item.date_change = datetime.utcnow()

            def check_empty_error(check_function, field_name, error_text, field_caption):
                if check_function(field_name):
                    return render_template('full_item.html', title=field_caption, item=item,
                                           field_with_error=field_name, error=error_text, select_fields=select_fields,
                                           select_aim=select_aim, select_urgency=select_urgency)

            def is_empty(f):
                return request.form[f].strip() is ''

            def is_negative(f):
                return int(request.form[f].strip()) < 1

            fields = [
                (is_empty, 'reagent_name', 'Заполните поле:  Наименование', 'Полное описание'),
                (is_empty, 'reagent_count', 'Заполните поле:  Количесво', 'Полное описание'),
                (is_negative, 'reagent_count', 'Количество не может быть меньше 1', 'Полное описание'),
                (is_empty, 'package', 'Заполните поле:  Фасовка', 'Полное описание'),
            ]

            for field in fields:
                check_f, field_name, error_text, field_caption = field
                error = check_empty_error(check_f, field_name, error_text, field_caption)
                if error:
                    return error

            db.session.commit()
            flash('Реагент обновлен')

    return render_template('full_item.html', title='Полное описание',
                           item=item, select_fields=select_fields,
                           select_aim=select_aim, select_urgency=select_urgency)


@app.route('/copy_item/<int:id>/', methods=['GET', 'POST'])
@login_required
def copy_item(id):
    item = ItemInOrder.query.get(id)
    reagent = ItemInOrder(author=current_user,
                          reagent_name=item.reagent_name, reagent_description=item.reagent_description,
                          package=item.package,
                          package_unit=item.package_unit, vendor_name=item.vendor_name,
                          catalogue_number=item.catalogue_number, url_reagent=item.url_reagent,
                          urgency=item.urgency, reagent_comments=item.reagent_comments,
                          reagent_aim=item.reagent_aim, reagent_count=item.reagent_count,
                          item_status_id='1')
    db.session.add(reagent)
    db.session.commit()
    flash('Реактив скопирован')

    return redirect(url_for('user'))


@app.route('/create_order', methods=['GET', 'POST'])
@admin_required
def create_order(form_checks=None):
    form = CreateOrderForm()
    numbers_list = Order.query.filter_by(number=form.number.data).first()
    form_checks = request.args.getlist('form_checks')
    order = 0
    # order = Order.query.order_by(Order.id.desc()).first()
    print(order)

    if form.validate_on_submit():
        if numbers_list:
            flash("Такой номер заказа уже существует, введите другой номер")
            return redirect(url_for('create_order'))
        order = Order(number=form.number.data, comment=form.comment.data, order_status_id='4')
        db.session.add(order)
        db.session.commit()
        x = order.id
        order_id = x

        flash('Заказ создан')
        if form_checks:
            for item_check in form_checks:
                check_id = int(item_check)
                reagent = ItemInOrder.query.get(check_id)
                reagent.reagent_in_order_id = order_id
                reagent.item_status_id = '4'
                db.session.commit()
                flash(f'Реагент { reagent.reagent_name } добавлен в заказ № {order.number}')
            return redirect(url_for('handling_items'))

        return redirect(url_for('create_order'))

    return render_template('orders/create_order.html', form=form, order=order)


@app.route('/checked_orders', methods=['GET', 'POST'])
@admin_required
def checked_orders(url=None, order_id=None):
    form_checks_order = request.form.getlist('checks')
    statuses = Status.query.all()
    items = ItemInOrder.query.filter_by(item_status_id='3').all()

    url = request.form.get('url')

    if '_add' in request.form:
        order_id = request.form.get('order_id')
        print(order_id)

        if items:
            if len(form_checks_order) == 1:
                order_id = int(form_checks_order[0])
                print(order_id)

                order = Order.query.get(order_id)
                return redirect(url_for('append_item', order_id=order_id))

            else:
                flash('Выберите только 1 заказ к которому необходимо добавить позиции')
        if not url:
            url = 'all_orders'
        else:
            flash('Не найдены заявки которые можно добавить к заказу')

    for s in statuses:
        action = s.action
        action_id = s.id
        action_flash = s.flashes

        if action in request.form:

            for order_check in form_checks_order:
                date = datetime.utcnow()
                check_id = int(order_check)
                order = Order.query.get(check_id)
                reagents_list = ItemInOrder.query.filter_by(reagent_in_order_id=check_id).all()
                order.order_status_id = action_id

                if reagents_list:
                    for reagent in reagents_list:
                        reagent.item_status_id = action_id
                        reagent.date_change = date

                if not reagents_list:
                    if '_del' in request.form:
                        db.session.delete(order)

            db.session.commit()
            flash(action_flash)

    return redirect(url_for(str(url)))


@app.route('/append_item', methods=['GET', 'POST'])
@admin_required
def append_item():
    items = ItemInOrder.query.filter_by(item_status_id='3').all()

    order_id = request.args.get('order_id') or request.form.get('order') or request.args.get('id')
    print(order_id)
    order = Order.query.filter_by(id=order_id)
    if not items:
        flash('Нет заявок в статусе Обработка. К заказу можно добавить только заявки в статусе Обработка.')
        return redirect(url_for('full_order', id=order_id))

    return render_template('items/append_item.html', items=items, id=order_id)


@app.route('/delete_item', methods=['GET', 'POST'])
@admin_required
def delete_item():
    order_id = request.args.get('order_id') or request.form.get('order') or request.args.get('id')
    print(order_id)
    items = ItemInOrder.query.filter_by(reagent_in_order_id=order_id).all()
    order = Order.query.filter_by(id=order_id)

    return render_template('items/append_item.html', items=items, id=order_id)


@app.route('/full_order/', methods=['GET', 'POST'], defaults={'id': -1})
@app.route('/full_order/<int:id>', methods=['GET', 'POST'])
@admin_required
def full_order(id):
    order = Order.query.get(id)
    items = ItemInOrder.query.filter_by(reagent_in_order_id=id).all()
    print(id, request.form)

    if '_delete_item' in request.form:
        id = request.form.get('oid')
        order = Order.query.get(id)
        checks = request.form.getlist('checks')
        print('delete', order, id, checks)
        for item_check in checks:
            check_id = int(item_check)
            item = ItemInOrder.query.get(check_id)
            item.reagent_in_order = None
            item.item_status_id = '3'
            db.session.commit()
            flash(f'Заявка { item.reagent_name } удалена из заказа № {order.number}')
        return redirect(url_for('full_order', id=id))

    return render_template('/orders/full_order.html', order=order, items=items, order_id=id)


@app.route('/report', methods=['GET', 'POST'])
@admin_required
def report():
    checked_fields = request.form.getlist('checks')

    items = ItemInOrder.query.filter_by(reagent_in_order_id='37').all()
    theads = []
    for field in checked_fields:
        pretty_field = format_const(field, REPORT_CHOICE)
        theads.append(pretty_field)

    for item in items:
        for field in checked_fields:
            if field == 'urgency':
                item.field = format_const(field, URGENCY)
                print(item.field)




    print(items)
    if '_report_csv' in request.form:
        csv_result = render_template('/items/_report.html', checked_fields=checked_fields, items=items, theads=theads)

        str_io = StringIO()
        str_io.write(csv_result)
        str_io.seek(0)

        mem_io = BytesIO(str_io.getvalue().encode('utf-8'))
        mem_io.write(str_io.getvalue().encode('utf-8'))
        mem_io.seek(0)
        str_io.close()

        return send_file(mem_io, mimetype="text/csv", as_attachment=True, attachment_filename="report.csv")


    return render_template('/items/custom_reports.html', checked_fields=checked_fields, items=items, theads=theads)




@app.route('/download_order/', methods=['GET', 'POST'])
@admin_required
def download_order():
    # id = request.form.get('oid')
    # items = ItemInOrder.query.filter_by(reagent_in_order_id=id).all()
    return send_file('order.csv',
                     attachment_filename='Order.csv',
                     as_attachment=True)


# 1 сооздать цсв как темплейт
# 2. отобразить его в браузере
# 3. контент диспозишн (пересмотреть видео ява скрип)
