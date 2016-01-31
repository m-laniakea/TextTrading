## App Initializer
#  Prepare for launch

from flask import Flask 
from flask.ext.moment import Moment
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from cfg import cfg

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()

def create_app(name):
    app = Flask(__name__)
    app.config.from_object(cfg[name])
    cfg[name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from .main import main as template
    app.register_blueprint(template)

    return app


