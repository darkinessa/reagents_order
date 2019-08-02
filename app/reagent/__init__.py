from flask import Blueprint

blueprint = Blueprint('reagent', __name__)

from app.reagent import routes
