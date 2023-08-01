from flask import Flask

from aider_app.blueprints.auth.oauth import github_blueprint

from .config import config
from .extensions import db
from .utils.base_endpoints import init_app_endpoints
from .utils.initializers import *


def create_app(cfg):

    app = Flask(__name__)

    app.config.from_object(cfg)

    register_extensions(app)
    register_blueprints(app)
    app.register_blueprint(github_blueprint, url_prefix='/auth/login')
    configure_db(app)
    init_app_endpoints(app)
    return app
