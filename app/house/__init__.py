from flask import Blueprint

bp = Blueprint('hse', __name__)

from app.house import routes, forms
