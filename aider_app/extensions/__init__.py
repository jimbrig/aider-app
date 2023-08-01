"""
Flask App Extensions

    - db: SQLAlchemy database instance.
    - migrate: Flask-Migrate instance.
    - bcrypt: Flask-Bcrypt instance.
    - login_manager: Flask-Login instance.
    - debug_toolbar: Flask-DebugToolbar instance.
    - csrf_protect: Flask-WTF CSRFProtect instance.
    - cors: Flask-CORS instance.
    - cache: Flask-Caching instance.
    - jwt: Flask-JWT-Extended instance.
    - celery: Celery instance.
    - limiter: Flask-Limiter instance.
    - babel: Flask-Babel instance.
    - admin: Flask-Admin instance.
    - rest_api: Flask-REST-JSONAPI instance.

"""

from .admin import admin
# from .bcrypt import bcrypt
# from .cache import cache
# from .cors import cors
from .csrf import csrf_protect
from .db import db
from .debug_toolbar import debug_toolbar
from .jwt import jwt
from .manager import login_manager
from .migrate import migrate

extensions = [
    admin,
    # bcrypt,
    # cache,
    # cors,
    # csrf_protect,
    # db,
    debug_toolbar,
    jwt,
    login_manager,
    migrate,
]
