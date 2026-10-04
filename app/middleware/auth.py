from flask import (Blueprint, redirect, session, url_for)
from ..controllers import user_controller


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=('GET', 'POST'))
def register():
    """Returns the register form page"""

    return user_controller.register()

@auth.route('/login', methods=('GET', 'POST'))
def login():
    """returns the login form page"""

    return user_controller.login()

@auth.route("/logout")
def logout():
    """clearing the current session, including the stored user id."""

    session.clear()
    return redirect(url_for("index"))