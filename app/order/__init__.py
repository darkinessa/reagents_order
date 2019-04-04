from flask import Blueprint

blueprint = Blueprint('order', __name__)

from app.order import routes
