## Define actions to take for route visited
#

from flask import render_template, redirect, url_for, session, current_app
from .. import db
from ..models import User
from . import main
from datetime import datetime


## 
# This is the index page (homepage)
# Here the user will be shown all of the initial content
##
@main.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())
    

