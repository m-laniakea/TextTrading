##
# Define actions to take for route visited
##

from flask import render_template, redirect, request, url_for, session, current_app, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User
from . import main
from . forms import LoginForm, SignupForm
from datetime import datetime

##
#
## Syntax for flashing: (display message in browser)
# 
#       flash('message', 'color_id')
#
#       color id's:
#
#       warning, success, danger, info
##


## 
# This is the index page (homepage)
# Here the user will be shown all of the initial content
##
@main.route('/', methods=['GET','POST'])
def index():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, True)
            flash('Welcome, ' + user.username + ".", 'success')
            return redirect(request.args.get('next') or url_for('main.index')) 
        flash('Invalid email + password combination.', 'danger')
    return render_template('index.html', current_time=datetime.utcnow(), form=form, show_user_navbar=True)


##
# Handle logout route
##
@main.route('/logout')
@login_required
def logout():
    logout_user()
    user = None
    flash('Logout successful', 'success')
    return redirect(url_for('main.index')) 

##
# Handle register route
##
@main.route('/register', methods=['GET','POST'])
def register():
    form = SignupForm()

    if current_user.is_authenticated:
        flash('You\'ve already registered, ' + current_user.username + '.', 'info')
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        new_user = User(email=form.email.data, username=form.username.data, set_password = form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, True)
        flash('Welcome to TextX, ' + new_user.username + '! You\'ve been logged in.', 'success')
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form, show_user_navbar=False)
    

