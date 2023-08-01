from flask import Blueprint

core_bp = Blueprint('core', __name__, static_folder='static', template_folder='templates')
