from app import app, db
from flask import redirect, render_template, url_for, flash, request
from app.order.models import ItemInOrder, Status
from app.order.forms import ReagentOrderForm
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
def delete_item(id):

    item = ItemInOrder.query.get(id)

    if item.item_status != Status.query.filter_by(id='1').all():
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

    form_checks = request.form.getlist('checks')
    statuses = Status.query.all()
#    print([(s.id, s.name, s.action, s.flashes) for s in statuses])
    for item in statuses:

        action = item.action
        action_id = item.id
        action_flash = item.flashes

        if action in request.form:
            for item_check in form_checks:
                check_id = int(item_check)
                reagent = ItemInOrder.query.get(check_id)
                reagent.item_status = Status.query.filter_by(id=str(action_id)).all()
                db.session.commit()
                flash(action_flash)

    if current_user.roles[0].is_admin():
        return redirect(url_for('admin'))

    else:

        return redirect(url_for('user'))
