## Define possible errors & actions to take

from . import main
from ..models import User
from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_user
from forms import LoginForm


##
# This page will be loaded when the server fails to find a requested page
##
@main.app_errorhandler(404)
def page_not_found(e):
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, True)
            flash('Welcome, ' + user.username + ".", 'success')
            return redirect(request.args.get('next') or url_for('main.index')) 
        flash('Invalid email + password combination.', 'danger')

    flash('The page requested could not be found. Here\'s a haiku instead.', 'info')
    return render_template('404.html', form=form), 404
