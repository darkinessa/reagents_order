

from app import app, db
from flask import redirect, render_template, url_for, flash, request

from app.auth.models import User
from app.order.models import ItemInOrder, Status
from app.order.forms import ReagentOrderForm
from app.auth.forms import LoginForm
from flask_login import current_user, login_required



@app.route('/item', methods=['GET', 'POST'])
@login_required
def item_add():
    form = ReagentOrderForm()

    if form.validate_on_submit():

        reagent = ItemInOrder(author=current_user,
                              reagent_name=form.reagent_name.data, package=form.package.data,
                              package_unit=form.package_unit.data, vendor_name=form.vendor_name.data,
                              catalogue_number=form.catalogue_number.data, url_reagent=form.url_reagent.data,
                              urgency=form.urgency.data, reagent_comments=form.reagent_comments.data,
                              reagent_aim=form.reagent_aim.data, reagent_count=form.reagent_count.data,
                              item_status=Status.query.filter_by(name='Черновик').all())
        db.session.add(reagent)
        db.session.commit()
        flash('Реактив добавлен в Заказ')
        return redirect(url_for('item_add'))

    return render_template('item.html', title='Добавление нового реактива', form=form)


@app.route('/delete_item/<int:id>', methods=['POST'])
@login_required
def del_draft_item(id):

    item = ItemInOrder.query.get(id)

    if item.item_status != Status.query.filter_by(name='Черновик').all():
        flash('Вы не можете удалить Реагент, который отправлен на обработку менеджеру')
        return redirect(url_for('user'))


    if item is None:
        flash('Реагент не найден')
        return redirect(url_for('user'))

    if current_user != item.author:
        print(current_user, item.author)
        flash('У вас нет прав на удаление этого реагента')
        return redirect(url_for('user'))

    db.session.delete(item)
    db.session.commit()
    flash('Реагент удален')
    return redirect(url_for('user'))


@app.route('/checked', methods=['GET', 'POST'])
@login_required
def checked():
    print(request)
    print(request.form)
    form_checks = request.form.getlist('checks')
    print(form_checks)

    action = '_send'
    action_1 = '_del'
    action_2 = '_sus'
    action_3 = '_dec'
    action_4 = '_hand'

    if action in request.form:
        for item_check in form_checks:
            check_id = int(item_check)
            item = ItemInOrder.query.get(check_id)
            print(item, item.item_status)

            item.item_status = Status.query.filter_by(id='2').all()
            db.session.commit()
            flash('Заказ отправлен на обработку менеджеру.')

    if action_1 in request.form:
        print('222')
        for item_check in form_checks:
            check_id = int(item_check)
            item = ItemInOrder.query.get(check_id)
            print(item, item.item_status)
            del_draft_item(id=check_id)

    if action_4 in request.form:
        for item_check in form_checks:
            check_id = int(item_check)
            item = ItemInOrder.query.get(check_id)
            print(item, item.item_status)

            item.item_status = Status.query.filter_by(id='3').all()
            db.session.commit()
            flash('Заказ принят')

    if action_2 in request.form:
        for item_check in form_checks:
            check_id = int(item_check)
            item = ItemInOrder.query.get(check_id)
            print(item, item.item_status)

            item.item_status = Status.query.filter_by(id='8').all()
            db.session.commit()
            flash('Отложен')

    if action_3 in request.form:
        for item_check in form_checks:
            check_id = int(item_check)
            item = ItemInOrder.query.get(check_id)
            print(item, item.item_status)

            item.item_status = Status.query.filter_by(id='7').all()
            db.session.commit()
            flash('Отложен')





    for item_check in form_checks:
        check_id = int(item_check)
        item = ItemInOrder.query.get(check_id)
        print(item)


    return redirect(url_for('user'))
