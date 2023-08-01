from flask_admin import Admin

from aider_app.extensions import db

admin = Admin(name='Admin', template_mode='bootstrap3', url='/admin')
