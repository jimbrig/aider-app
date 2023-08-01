import os
import random
import string


class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Asset Mgmt
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')

    # Flask Secret Key
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))

    # Social AUTH
    SOCIAL_AUTH_GITHUB = False
    GITHUB_ID = os.getenv('GITHUB_ID', None)
    GITHUB_SECRET = os.getenv('GITHUB_SECRET', None)

    if GITHUB_ID and GITHUB_SECRET:
        SOCIAL_AUTH_GITHUB = True

    SOCIAL_AUTH_TWITTER = False
    TWITTER_ID = os.getenv('TWITTER_ID', None)
    TWITTER_SECRET = os.getenv('TWITTER_SECRET', None)

    if TWITTER_ID and TWITTER_SECRET:
        SOCIAL_AUTH_TWITTER = True

    # Database
    DB_ENGINE   = os.getenv('DB_ENGINE'   , None)
    DB_USERNAME = os.getenv('DB_USERNAME' , None)
    DB_PASS     = os.getenv('DB_PASS'     , None)
    DB_HOST     = os.getenv('DB_HOST'     , None)
    DB_PORT     = os.getenv('DB_PORT'     , None)
    DB_NAME     = os.getenv('DB_NAME'     , None)

    DB_USE_SQLITE = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', None)

    if DB_ENGINE and DB_NAME and DB_USERNAME:

        try:
            SQLALCHEMY_DATABASE_URI = f"{DB_ENGINE}://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            DB_USE_SQLITE = False
        except Exception as e:
            print(f">>> [Error]: Database Exception: {str(e)}")
            print(f">>> [Info]: Fallback to SQLite Database: URI is {SQLALCHEMY_DATABASE_URI}")

    if DB_USE_SQLITE:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


class DebugConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Security
    SESSION_COOKIE_HTTPONLY = False
    REMEMBER_COOKIE_HTTPONLY = False
    REMEMBER_COOKIE_DURATION = 3600

    # Flask Debug Toolbar
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.basedir, 'db.sqlite3')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Debug Toolbar
    DEBUG_TB_ENABLED = False
    WTF_CSRF_ENABLED = False

    # Security
    SESSION_COOKIE_HTTPONLY = False
    REMEMBER_COOKIE_HTTPONLY = False
    REMEMBER_COOKIE_DURATION = 3600


config = {
    'Debug': DebugConfig,
    'Production': ProdConfig,
    'Testing': TestConfig
}

