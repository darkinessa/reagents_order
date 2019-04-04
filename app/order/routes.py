from app import app, db
from flask import redirect, render_template, url_for
from app.order.models import Reagent
from app.order.forms import ReagentForm


@app.route('/reagent_get', methods=['GET', 'POST'])
def reagent_get():
    form = ReagentForm()
    if form.validate_on_submit():
        reagent = Reagent(reagent_name=form.reagent_name.data,
                vendor_name=form.vendor_name.data,
                reagent_catalog=form.reagent_catalog.data,
                url_reagent=form.url_reagent.data)
        db.session.add(reagent)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('reagent_get.html', title='Заказ нового реактив', form=form)
