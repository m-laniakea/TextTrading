## Define possible errors & actions to take

from . import main
from flask import render_template


##
# This page will be loaded when the server fails to find a requested page
##
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
