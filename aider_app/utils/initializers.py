import os

from flask import Flask

from aider_app.extensions import db, extensions, login_manager


def register_extensions(app):
    """Registers all extensions."""

    db.init_app(app)

    login_manager.init_app(app)

    # for ext in extensions:
    #     if hasattr(ext, 'init_app'):
    #         app = ext.init_app(app)

    #     else:
    #         ext.init_app(app)

    return app


def register_blueprints(app):
    """Registers all blueprints."""
    from aider_app.blueprints import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)
    return app


def configure_db(app):
    """Configures the database."""

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print(f">>> [Error]: Database Exception: {str(e)}")

            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print(f">>> [Info]: Fallback to SQLite Database: URI is {SQLALCHEMY_DATABASE_URI}")
            db.create_all()


    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()



    from aider_app.extensions import db
    db.init_app(app)
    return app
