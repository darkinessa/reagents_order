from app import app, db
from flask import flash, redirect, url_for
from flask_login import current_user
from functools import wraps

from app.admin.constants import SUPER_ADMIN_EMAILS


def super_admin_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not current_user.email or current_user.email not in SUPER_ADMIN_EMAILS:
            return redirect(url_for('index'))
        return func(*args, **kwargs)

    return wrapped


@app.template_filter('super_admin')
def super_admin(func):
    if not current_user.email or current_user.email not in SUPER_ADMIN_EMAILS:
        return False
    return True


def admin_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not current_user.admin:
            if not current_user.email or current_user.email not in SUPER_ADMIN_EMAILS:
                return redirect(url_for('index'))
        return func(*args, **kwargs)

    return wrapped


@app.template_filter('is_admin')
def is_admin(func):
    if not current_user.admin:
        return False
    return True
