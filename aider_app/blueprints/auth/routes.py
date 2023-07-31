from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Add your login logic here
    return 'Login route'

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Add your register logic here
    return 'Register route'
