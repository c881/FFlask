from flask import Blueprint

auth = Blueprint('auth',__name__)


@auth.route('/login')
def hello():
    return "<p>Login</p>"


@auth.route('/logout')
def hello():
    return "<p>Logout</p>"


@auth.route('/sign-up')
def hello():
    return "<p>Sign-Up</p>"