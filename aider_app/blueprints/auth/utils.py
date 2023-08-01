#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""auth/utils.py

Utility functions for the auth blueprint.

  - check_password: Checks if the password is valid.
  - generate_password_hash: Generates a password hash.
  - authenticate: Authenticates a user.
  - create_token: Creates a JWT token.
  - get_logged_in_user: Gets the logged in user.
  - login_required: Decorator to ensure that a user is logged in.

"""

import binascii
import hashlib
import os


def check_password(hashed_password, password):
    """Checks if the password is valid.

    Args:
        hashed_password (str): The hashed password.
        password (str): The password to check.

    Returns:
        bool: True if the password is valid, False otherwise.

    """
    from werkzeug.security import check_password_hash
    return check_password_hash(hashed_password, password)


def generate_password_hash(password):
    """Generates a password hash.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.

    """
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)


def authenticate(username, password):
    """Authenticates a user.

    Args:
        username (str): The username.
        password (str): The password.

    Returns:
        User: The authenticated user.

    """
    from aider_app.models.core import User
    user = User.query.filter_by(username=username).first()
    if user and check_password(user.password, password):
        return user
    return None


def create_token(user):
    """Creates a JWT token.

    Args:
        user (User): The user to create the token for.

    Returns:
        str: The JWT token.

    """
    from flask_jwt_extended import create_access_token
    return create_access_token(identity=user.username)


def get_logged_in_user():
    """Gets the logged in user.

    Returns:
        User: The logged in user.

    """
    from flask_jwt_extended import get_jwt_identity

    from aider_app.models.core import User
    username = get_jwt_identity()
    return username and User.query.filter_by(username=username).first()


def hash_password(password):
    """Hashes a password.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.

    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                    salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)


def verify_password(provided_password, stored_password):
    """Verifies a password.

    Args:
        provided_password (str): The password to verify.
        stored_password (str): The stored password.

    Returns:
        bool: True if the password is valid, False otherwise.

    """
    salt = stored_password[:64]
    stored_password = stored_password.decode('ascii')[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha256',
                                    provided_password.encode('utf-8'),
                                    salt.encode('ascii'),
                                    100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password
