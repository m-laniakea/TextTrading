## Define actions to take for route visited
#

from flask import render_template, redirect, url_for, session, current_app, flash
from .. import db
from ..models import User
from . import main
from datetime import datetime


## 
# This is the index page (homepage)
# Here the user will be shown all of the initial content
##
@main.route('/', methods=['GET','POST'])
def index():
    flash("Hello, user alerts are indeed working.",'success')
    flash("You can close this alert by clicking the x.", 'warning')
    #flash("Oh no! Something went wrong", 'danger')
    return render_template('index.html', current_time=datetime.utcnow())
    

