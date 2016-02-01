## Define possible errors & actions to take

from . import main
from flask import render_template, flash
from forms import LoginForm


##
# This page will be loaded when the server fails to find a requested page
##
@main.app_errorhandler(404)
def page_not_found(e):
    form = LoginForm()
    flash('The page requested could not be found. Here\'s a haiku instead.', 'info')
    return render_template('404.html', form=form), 404
