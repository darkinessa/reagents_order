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
    reagent_form = ReagentForm()
    reagent = Reagent(reagent_name=reagent_form.reagent_name.data, 
                vendor_name=reagent_form.vendor_name.data, 
                catalogue_number=reagent_form.catalogue_number.data,
                url_reagent=reagent_form.url_reagent.data)

    db.session.add(reagent)

    db.session.commit()

    return render_template('reagent_get.html', title='Заказ нового реактива', form=reagent_form)



