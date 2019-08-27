from datetime import datetime

from app import app, db
from flask import redirect, render_template, url_for, flash, request

from app.auth.decorators import active_user_required
from app.order.constants import URGENCY, AIM, format_const
from app.order.models import ItemInOrder, Status
from app.order.forms import ReagentOrderForm
from flask_login import current_user, login_required


@app.route('/item', methods=['GET', 'POST'])
@login_required
@active_user_required
def item_add():
    form = ReagentOrderForm()
    print(form.reagent_aim.data, form.reagent_aim.data)

    if form.validate_on_submit():
        reagent = ItemInOrder(author=current_user,
                              reagent_name=form.reagent_name.data,reagent_description=form.reagent_description.data, package=form.package.data,
                              package_unit=form.package_unit.data, vendor_name=form.vendor_name.data,
                              catalogue_number=form.catalogue_number.data, url_reagent=form.url_reagent.data,
                              urgency=int(form.urgency.data), author_comments=form.author_comments.data,
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
def checked():
    form_checks = request.form.getlist('checks')
    print(form_checks)
    statuses = Status.query.all()
    print([(s.id, s.name, s.action, s.flashes) for s in statuses])
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

    if current_user.admin:
        return redirect(url_for('admin'))

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
                                  reagent_name=item.reagent_name, reagent_description=item.reagent_description, package=item.package,
                                  package_unit=item.package_unit, vendor_name=item.vendor_name,
                                  catalogue_number=item.catalogue_number, url_reagent=item.url_reagent,
                                  urgency=item.urgency, author_comments=item.author_comments,
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
                          reagent_name=item.reagent_name, reagent_description=item.reagent_description, package=item.package,
                          package_unit=item.package_unit, vendor_name=item.vendor_name,
                          catalogue_number=item.catalogue_number, url_reagent=item.url_reagent,
                          urgency=item.urgency, reagent_comments=item.reagent_comments,
                          reagent_aim=item.reagent_aim, reagent_count=item.reagent_count,
                          item_status_id='1')
    db.session.add(reagent)
    db.session.commit()
    flash('Реактив скопирован')

    return redirect(url_for('user'))
