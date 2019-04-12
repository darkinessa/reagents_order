from app import app, db
from flask import redirect, render_template, url_for, flash
from app.order.models import ItemInOrder
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
                              reagent_aim=form.reagent_aim.data)
        db.session.add(reagent)
        db.session.commit()
        flash('Реактив добавлен в Заказ')
        return redirect(url_for('item_add'))

    return render_template('item.html', title='Добавление нового реактива', form=form)
