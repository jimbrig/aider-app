from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_dance.contrib.github import github
from flask_login import current_user, login_user, logout_user

from aider_app.blueprints.auth import auth_bp
from aider_app.blueprints.auth.forms import CreateAccountForm, LoginForm
from aider_app.blueprints.auth.models import OAuth, Users
from aider_app.blueprints.auth.oauth import github_blueprint
from aider_app.blueprints.auth.utils import verify_password
from aider_app.extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@auth_bp.route('/')
def route_default():
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/github')
def github_login():
    if not github_blueprint.authorized:
        return redirect(url_for('github.login'))

    resp = github_blueprint.get('/user')
    assert resp.ok

    return redirect(url_for('home_bp.index'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        user_id = request.form['username']
        password = request.form['password']

        user = Users.find_by_username(user_id)

        if not user:
            user = Users.find_by_email(user_id)

            if not user:
                return render_template('auth/login.html', msg='User not found', form=login_form)

        if verify_password(password, user.password):
            login_user(user)
            return redirect(url_for('auth_bp.route_default'))

        return render_template('auth/login.html', msg='Wrong password', form=login_form)


    if not Users.current_user.is_authenticated:
        return render_template('auth/login.html', form=login_form)


    return redirect(url_for('core_bp.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('auth/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('auth/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template('auth/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('auth/register.html', form=create_account_form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('auth/errors/403.html'), 403


@auth_bp.errorhandler(403)
def access_forbidden(error):
    return render_template('auth/errors/403.html'), 403


@auth_bp.errorhandler(404)
def not_found_error(error):
    return render_template('auth/errors/404.html'), 404


@auth_bp.errorhandler(500)
def internal_error(error):
    return render_template('auth/errors/500.html'), 500
