import os

from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage import MemoryStorage
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.github import github, make_github_blueprint
from flask_login import current_user, login_user
from sqlalchemy.exc import NoResultFound

from aider_app.blueprints.auth.models import OAuth, Users
from aider_app.config import Config
from aider_app.extensions import db

github_blueprint = make_github_blueprint(
    client_id=Config.GITHUB_ID,
    client_secret=Config.GITHUB_SECRET,
    scope='user',
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    ),
)


@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):

    info = github_blueprint.get('/user')

    if info.ok:

        account_info = info.json()
        username = account_info['login']

        query = Users.query.filter_by(username=username)

        try:

            user = query.one()
            login_user(user)

        except NoResultFound:

            # Save to DB
            user = Users()
            user.username = '(gh)' + username
            user.oauth_github = username

            # Save current user
            db.session.add(user)
            db.session.commit()

            login_user(user)
