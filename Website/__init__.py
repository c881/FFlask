from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session

def create_app():
    app = Flask(__name__)

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    # app.config["SESSION_PERMANENT"] = False
    # app.config["SESSION_TYPE"] = "filesystem"
    return app



# Session(app)

# db = SQL("sqlite:///sample.db")
