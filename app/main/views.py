## Define actions to take for route visited
#

from flask import render_template, redirect, request, url_for, session, current_app, flash
from flask.ext.login import login_user
from .. import db
from ..models import User
from . import main
from . forms import LoginForm
from datetime import datetime


## 
# This is the index page (homepage)
# Here the user will be shown all of the initial content
##
@main.route('/', methods=['GET','POST'])
def index():
    form = LoginForm()
    flash("Hello, user alerts are indeed working.",'success')
    flash("You can close this alert by clicking the x.", 'warning')
    #flash("Oh no! Something went wrong", 'danger')
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, True)
            return redirect(request.args.get('next') or url_for('main.index')) 
        flash('Invalid email + password combination.', 'danger')

    return render_template('index.html', current_time=datetime.utcnow(), form=form)
    

