##
# Define actions to take for route visited
##

from flask import render_template, redirect, request, url_for, session, current_app, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User, Book, Conversation, Message
from . import main
from . forms import LoginForm, SignupForm, BookForm, MessageForm, ConvInitForm, flash_errors, process_login
from datetime import datetime
from sqlalchemy import or_

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
    current_user.is_online = False
    db.session.commit()
    logout_user()
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
        return redirect(url_for('main.profile', username=current_user.username))

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
        conversations = user.conversations
        return render_template('profile.html', form=form, user=user, books=books, conversations=conversations)

    flash("\"" + username + '\" is not a member yet.', 'info')
    abort(404)
    
##
# Individual Books route
# View book entry where url is unique identifier
##
@main.route('/b/<bookid>', methods=['GET', 'POST'])
def book(bookid):
    form = LoginForm()
    form2 = ConvInitForm()

    if form.validate_on_submit():
        process_login(form)

    book = Book.query.get(int(bookid))

    if form2.validate_on_submit():
        c = Conversation(subject=book.title, book_id=book.id)
        c.participants.append(current_user)
        c.participants.append(book.owner)
        m = Message(contents = "I'm interested in your book \"" + book.title + "\".", sender=current_user.username, conversation=c)

        db.session.add(c)
        db.session.add(m)
        db.session.commit()
        
        flash('Trade request sent to ' + book.owner.username, 'success')
        return redirect(url_for('main.conversation', cid = c.id))


    if book:
        owner = User.query.get(book.owner_id)
        return render_template('book.html', form=form, form2=form2, book=book, owner=owner)

    flash("This book does not exist.", "info")
    abort(404)





##
# Deletion route
##
@main.route('/d/<t>/<iid>')
def delete_book(t, iid):
    
    if current_user.is_anonymous:
        flash("You must be logged-in to delete items.", "info")
        return redirect(url_for('main.index'))

    # If the item to be deleted is a conversation
    if t == "c":
        c = Conversation.query.get(int(iid))
        if c:
            # if requestor is not a participant
            if not current_user in c.participants:
                flash("Only conversation participants may delete conversations.", 'warning')


            else: 
                flash('Conversation regarding \"' + c.subject + '\" successfully removed', 'success')
                for m in c.messages:
                    db.session.delete(m)

                db.session.delete(c)

                db.session.commit()
            return redirect(url_for('main.profile', username = current_user.username))



    # If deletion type book
    elif t == "b":

        book = Book.query.get(int(iid))

        if book:
            if book.owner_id == current_user.id:
                db.session.delete(book)
                db.session.commit()
                flash('\"' + book.title + '\" successfully deleted.', "success")
        
            else:
                flash("Only the owner may delete their book.", "warning")

        return redirect(url_for('main.profile', username = current_user.username))

    flash("This item does not exist.", "info")
    abort(404)


##
# Book editing route
# (Currently only for adding)
##
@main.route('/add', methods=['GET', 'POST'])
def edit_book():

    form = BookForm()

    if current_user.is_anonymous:
        flash("You must be logged-in to add books.", "info")
        return redirect(url_for('main.index'))


    if form.validate_on_submit():
        b = Book(title=form.title.data, author=form.author.data, condition=form.condition.data,
                isbn=form.isbn.data, price=form.price.data, owner_id=current_user.id)

        db.session.add(b)
        db.session.commit()
        flash("Book added successfully", "success")
        return redirect(url_for('main.profile', username=current_user.username))

    flash_errors(form)
    return render_template("bookform.html", form=form)



##
# Book browsing route
##
@main.route('/books', methods=['GET','POST'])
def books():

    if request.method == 'POST':
        return search();
    else:
        allbooks = Book.query.order_by("id desc")
        form = LoginForm()       
        
        if form.validate_on_submit():
            process_login(form)
        
        return render_template('browse.html', form=form, allbooks=allbooks)


##
# Conversation route
##
@main.route('/c/<cid>', methods=['GET', 'POST'])
def conversation(cid):

    form = MessageForm()


    if current_user.is_anonymous:
        flash('You must be logged in to view your conversations.', 'info')
        return redirect(url_for('main.index'))

    conversation = Conversation.query.get(cid)

    if not conversation:
        flash("This conversation never took place", 'info')
        abort(404)

    # Send message
    if form.validate_on_submit():
        m = Message(contents=form.text.data, sender=current_user.username)
        conversation.messages.append(m)
        db.session.commit()
        # Blank field for next submission
        form.text.data =""


    for p in conversation.participants:
        if current_user == p:
            return render_template("conversation.html", conversation=conversation, messages=messages, form=form)

    flash('Only conversation participants may view this page.', 'warning')
    # Redirect to previous  path
    return redirect(request.referrer)

##
# Searches database with user given search parameters. 
##
def search():
    search = request.form['search'];
    if len(request.form['search']) > 0:
        #Seaches if title contains the search parameter and then searches isbn 
        allbooks = Book.query.filter(Book.title.contains(search) | Book.isbn.contains(search) | Book.author.contains(search));

    else:
        allbooks = Book.query.order_by("id desc")

    return render_template('browse.html', form="", allbooks=allbooks);
    









