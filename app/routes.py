from app import app, db
from app.forms import ReagentForm
from flask import flash, redirect, render_template, url_for
from flask_wtf import FlaskForm
from app.models import Reagent, ItemInOrder


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')




@app.route('/reagent_get', methods=['GET', 'POST']) # reagent_get показывает путь к странице
def reagent_get():
    print("DEBUG 1")
    reagent_form = ReagentForm()
    print(reagent_form.reagent_name.validate(reagent_form))
    # print(reagent_form.vendor_name.validate(reagent_form))
    # print(reagent_form.catalogue_number.validate(reagent_form))
    # print(reagent_form.url_reagent.validate(reagent_form))
    

    
    reagent = Reagent(reagent_name=reagent_form.reagent_name.data)
    print(reagent)
    print(reagent_form.validate())
    if reagent_form.validate_on_submit():
        print("DEBUG 2")
        reagent = Reagent(reagent_name=reagent_form.reagent_name.data)
        print("DEBUG 3")
        db.session.add(reagent)

        db.session.commit()
        flash('ddd')
        return redirect(url_for('reagent_get'))
    else:
        print("DEBUG4")
    return render_template('reagent_get.html', title='Заказ нового реактива', form=reagent_form)


# if reagent_form.validate_on_submit():
