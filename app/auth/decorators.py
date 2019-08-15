from app import app, db
from flask import flash, redirect, url_for
from flask_login import current_user
from functools import wraps


@app.template_filter('is_active')
def is_active(func):
    if current_user.is_authenticated:
        if current_user.role == 2:
            return True
        return False
    return False


def active_user_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not current_user or current_user.role != 2:
            flash('Ваша учетная запись не активирована, дождитесь активации или свяжитесь с менеджером сайта')
            return redirect(url_for('index'))
        return func(*args, **kwargs)

    return wrapped
