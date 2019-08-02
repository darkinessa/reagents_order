from app import app, db
from flask import redirect, render_template, url_for, flash
from app.reagent.models import Reagent
from app.reagent.forms import ReagentForm


@app.route('/reagent_add', methods=['GET', 'POST'])
def reagent_add():
    form = ReagentForm()
    if form.validate_on_submit():
        reagent = Reagent(reagent_name=form.reagent_name.data, package=form.package.data,
                          package_unit=form.package_unit.data, vendor_name=form.vendor_name.data,
                          catalogue_number=form.catalogue_number.data, url_reagent=form.url_reagent.data,
                          reagent_comments=form.reagent_comments.data)
        db.session.add(reagent)
        db.session.commit()
        flash('Реактив добавлен в Базу')
        return redirect(url_for('reagent_add'))

    return render_template('reagent_add.html', title='Добавление нового реактива', form=form)
