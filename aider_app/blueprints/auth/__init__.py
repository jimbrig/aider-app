# from .routes import auth_bp

from flask import Blueprint

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth', static_folder='static', template_folder='templates')
