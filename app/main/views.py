##
# Define actions to take for route visited
##

from flask import render_template, redirect, request, url_for, session, current_app, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User, Book
from . import main
from . forms import LoginForm, SignupForm, flash_errors, process_login
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
#
#
## form.validate_on_submit() returns True 
#    if input was successfully validated
##


## 
# This is the index page (homepage)
# Here the user will be shown all of the initial content
##
@main.route('/', methods=['GET','POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        if process_login(form):
            # Redirect user to their profile
            return redirect(url_for('main.profile', username = current_user.username))
    
    return render_template('index.html', current_time=datetime.utcnow(), form=form)


##
# Handle logout route
##
@main.route('/logout')
@login_required
def logout():
    current_user.last_online = datetime.utcnow()
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
        new_user = User(email=form.email.data.lower(), username=form.username.data, set_password = form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, True)
        flash('Welcome to TextX, ' + new_user.username + '! You\'ve been logged in.', 'success')
        return redirect(url_for('main.index'))

    # Flash form errors for user
    flash_errors(form)
    return render_template('register.html', form=form, disable_user_login=True)


##
# Handle user profiles route
##
@main.route('/u/<username>', methods=['GET', 'POST'])
def profile(username):
    form = LoginForm()

    if form.validate_on_submit():
        process_login(form)

    user = User.query.filter_by(username=username).first()
    if user:
        books = user.books.all()
        return render_template('profile.html', form=form, user=user, books=books)

    flash("\"" + username + '\" is not a member yet.', 'info')
    abort(404)
    
##
# Individual Books route
# View book entry where url is unique identifier
##
@main.route('/b/<bookid>', methods=['GET', 'POST'])
def book(bookid):
    form = LoginForm()

    if form.validate_on_submit():
        process_login(form)

    book = Book.query.get(int(bookid))

    if book:
        owner = User.query.get(book.owner_id)
        return render_template('book.html', form=form, book=book, owner=owner)

    flash("This book does not exist.", "info")
    abort(404)
