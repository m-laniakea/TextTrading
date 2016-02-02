##
# App Initializer
# Prepare for launch
##

from flask import Flask 
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from cfg import cfg

login_manager = LoginManager()
db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()

login_manager.session_protection = 'strong'

def create_app(name):
    app = Flask(__name__)
    app.config.from_object(cfg[name])
    cfg[name].init_app(app)

    login_manager.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    ##
    # Prepare blueprint for use in main/__init__.py
    ##
    from .main import main as template
    app.register_blueprint(template)

    return app


