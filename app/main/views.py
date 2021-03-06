##
# Define actions to take for route visited
##

from flask import render_template, redirect, request, url_for, session, current_app, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User, Book, Conversation, Message, Vote
from . import main
from . forms import LoginForm, SignupForm, BookForm, MessageForm, ConvInitForm, SearchForm, EditProfileForm, flash_errors, process_login
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
    current_user.is_online = False
    db.session.commit()
    logout_user()
    flash('Logout successful', 'success')
    return redirect( url_for('main.index') ) 

##
# Handle register route
##
@main.route('/register', methods=['GET','POST'])
def register():
    form = SignupForm()

    if current_user.is_authenticated:
        flash('You\'ve already registered, ' + current_user.username + '.', 'info')
        return redirect( url_for('main.index') )

    if form.validate_on_submit():
        new_user = User(email=form.email.data.lower(), username=form.username.data, set_password = form.password.data, location=form.location.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, True)
        flash('Welcome to TextX, ' + new_user.username + '! You\'ve been logged in.', 'success')
        return redirect( url_for('main.profile', username=current_user.username) )

    # Flash form errors for user
    flash_errors(form)
    return render_template('register.html', form=form, disable_user_login=True)

@main.route('/editprofile', methods=['GET','POST'])
def editprofile():
    form = EditProfileForm()
    form.location.data = current_user.location
    form.username.data = current_user.username
    form.email.data = current_user.email

    if not current_user.is_authenticated:
        return render_template('editprofile.html', form=form)

    if form.validate_on_submit():
        current_user.set_password = form.password.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Password has been changed!')
        return redirect( url_for('main.profile', username=current_user.username))

    flash_errors(form)
    return render_template('editprofile.html', form=form)


##
# Handle user profiles route
##
@main.route('/u/<username>', methods=['GET', 'POST'])
def profile(username):
    form = LoginForm()

    if form.validate_on_submit():
        process_login(form)

    user = User.query.filter_by(username=username).first()

    # If this user exists
    if user:
        books = user.books.all()
        conversations = user.conversations
        rating = user.show_rating()
        return render_template('profile.html', form=form, user=user, books=books, conversations=conversations, rating=rating)

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
        return redirect( url_for('main.book', bookid=bookid) )

    book = Book.query.get( int(bookid) )

    # User has hit the "Contact Owner" button
    if form2.validate_on_submit():
        
        if book.owner == current_user:
            return redirect( url_for('main.book', bookid=book.id) )

        c = Conversation(subject=book.title, book_id=book.id)
        c.participants.append(current_user)
        c.participants.append(book.owner)
        m = Message(contents = "I'm interested in your book \"" + book.title + "\".", sender=current_user.username, conversation=c)

        # Add conversation to db
        db.session.add(c)
        db.session.commit()
        
        flash('Trade request sent to ' + book.owner.username, 'success')
        return redirect( url_for('main.conversation', cid = c.id) )


    # If the book exists
    if book:
        owner = User.query.get(book.owner_id)
        rating = owner.show_rating()
        return render_template('book.html', form=form, form2=form2, book=book, owner=owner, rating=rating)

    flash("This book does not exist.", "info")
    abort(404)



##
# Deletion route
#
# <t> gives the type of object to delete
# <iid> represents the item id
##
@main.route('/d/<t>/<iid>')
def delete_book(t, iid):
    
    if current_user.is_anonymous:
        flash("You must be logged-in to delete items.", "info")
        return redirect( url_for('main.index') )

    # If the item to be deleted is a conversation
    if t == "c":
        c = Conversation.query.get( int(iid) )
        # If this conversation exists
        if c:
            # if requestor is not a participant
            if not current_user in c.participants:
                flash("Only conversation participants may delete conversations.", 'warning')

            else: 
                flash('Conversation regarding \"' + c.subject + '\" successfully removed', 'success')

                # Delete all mesages in the conversation
                for m in c.messages:
                    db.session.delete(m)

                db.session.delete(c)

                db.session.commit()

            return redirect( url_for('main.profile', username = current_user.username) )



    # If deletion type book
    elif t == "b":

        book = Book.query.get( int(iid) )

        # If book exists
        if book:

            if book.owner_id == current_user.id:
                db.session.delete(book)
                db.session.commit()
                flash('\"' + book.title + '\" successfully deleted.', "success")
        
            else:
                flash("Only the owner may delete their book.", "warning")

        return redirect( url_for('main.profile', username = current_user.username) )

    # Item was none of the supported deletion types
    flash("This item does not exist.", "info")
    abort(404)


##
# Add book route
##
@main.route('/add', methods=['GET', 'POST'])
def edit_book():

    form = BookForm()

    if current_user.is_anonymous:
        flash("You must be logged-in to add books.", "info")
        return redirect( url_for('main.index') )

    # User has hit "Save" on BookForm
    if form.validate_on_submit():
        b = Book(title=form.title.data, author=form.author.data, 
                condition=form.condition.data, isbn=form.isbn.data, 
                price=form.price.data, owner_id=current_user.id)

        db.session.add(b)
        db.session.commit()
        flash("Book added successfully", "success")

        # Return user to their profile
        return redirect( url_for('main.profile', username=current_user.username) )

    # Render errors from BookForm if present
    flash_errors(form)
    return render_template("bookform.html", form=form)


   
##
# Edit books route
##
@main.route('/add/<bookid>', methods=['GET', 'POST'])
def modify_book(bookid):
    form = BookForm()

    book = Book.query.get( int(bookid) )
    print book
    

    if current_user.is_anonymous:
        flash("You must be logged-in to edit books.", "info")
        return redirect( url_for('main.index') )

    # User has hit "Save" on BookForm
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.price = form.price.data
        book.isbn = form.isbn.data
        book.condition = form.condition.data

        db.session.commit()
        flash("Book has been successfully edited", "success")

        # Return user to their profile
        return redirect( url_for('main.profile', username=current_user.username) )



    form.author.data = book.author
    form.price.data = book.price
    form.isbn.data = book.isbn
    form.condition.data = book.condition
    form.title.data = book.title
  

    # Render errors from BookForm if present
    flash_errors(form)
    return render_template("bookform.html", form=form, book=book)


##
# Conversation route
##
@main.route('/c/<cid>', methods=['GET', 'POST'])
def conversation(cid):

    form = MessageForm()


    if current_user.is_anonymous:
        flash('You must be logged in to view your conversations.', 'info')
        return redirect( url_for('main.index') )

    conversation = Conversation.query.get(cid)

    if not conversation:
        flash("This conversation never took place", 'info')
        abort(404)

    # Send message
    if form.validate_on_submit():
        m = Message(contents=form.text.data, sender=current_user.username)
        conversation.messages.append(m)
        db.session.commit()
        # Blank out field for next submission
        form.text.data =""

    ##
    # Check if user is a participants
    # and may view this conversation
    ##
    for p in conversation.participants:
        if current_user == p:
            messages = conversation.messages
            return render_template("conversation.html", conversation=conversation, messages=messages, form=form)

    flash('Only conversation participants may view this page.', 'warning')
    # Redirect to previous  path
    return redirect(request.referrer)
 

##
# Book browsing route
##
@main.route('/books', methods=['GET','POST'])
def books():
 

    form = LoginForm()       
    # Search submit button
    s_form = SearchForm()
    
    # If user hit login
    if form.validate_on_submit():
        process_login(form)
        return redirect('/books')


    if not s_form.location.data:
        # Get user's location
        if current_user.is_authenticated:
            s_form.location.data = current_user.location

        # If user's location unknown, load the default
        else:
            s_form.location.data = "University of Washington - Bothell"



    # If user hit "search"
    if s_form.validate_on_submit():
        return search()
    else:
        allbooks = Book.query.order_by("id desc")
      
    return render_template('browse.html', form=form, s_form=s_form, allbooks=allbooks, searchState="All Books at " + s_form.location.data)


##
# Searches database with user given search parameters. 
##
def search():
    form = LoginForm()
    # Search submit form
    s_form = SearchForm()
    
    # User has hit login
    if form.validate_on_submit():
        process_login(form)

    # If no location data entered
    if not s_form.location.data:
        # Get user's location
        if current_user.is_authenticated:
            s_form.location.data = current_user.location

        # If user's location unknown, load the default
        else:
            s_form.location.data = "University of Washington - Bothell"
        
        flash("No location entered. Using " + s_form.location.data, 'info')


    search = s_form.search.data
    location = s_form.location.data 
    searchState = "All Books"

    if len(search) > 0:
        # Searches if title contains the search parameter
        allbooks = Book.query.filter( Book.owner.has(location=location), Book.title.contains(search) | Book.isbn.contains(search) | Book.author.contains(search) );

        searchState = 'Results for \"'+ search + '\"';
    else:
        # User has entered a blank search, just display all books
        allbooks = Book.query.filter.Book.owner.has(location=location).order_by("id desc")

    return render_template('browse.html', form=form, s_form=s_form, allbooks=allbooks, searchState=searchState);
    

##
# User rating route
#
# <uid> represents the user id to be voted
#
# if <positive> is true, rating is positive
##
@main.route('/r/<uid>/<positive>')
def rate_user(uid, positive):

    if current_user.is_anonymous:
        flash('You must be logged in to rate users.', 'info')
        return redirect( url_for('main.index') )

    user = User.query.filter_by(id=uid).first()
    
    # if user exists
    if user:
        if current_user == user:
            flash('You cannot rate yourself.', 'warning')

        # Check if valid rating was passed
        elif positive == "True" or positive == "False":
            rating = True if positive == 'True' else False
        
            old_vote = False 

            # Check if current user has rated this user
            for v in current_user.voted_for:
                if v.voted_for == user:
                    # Get vote last cast
                    old_vote = v
                    break

            # If vote already cast for this user
            if old_vote:
                # If new vote is same as old
                if rating == old_vote.positive:
                    flash('You already gave this vote to ' + user.username + '.', 'info')
                    return redirect( url_for('main.profile', username=user.username) )
                
                # New vote is different, adjust users rating
                user.adjust_rating(old_vote.positive)
                # Save changed vote
                old_vote.positive = rating
                db.session.commit()
                flash('Rating for ' + user.username + ' successfully updated.', 'success')
            
            # User is casting a brand new vote
            else:
                user.add_rating(rating)
                vote = Vote(voted_for=user, voted_by=current_user, positive=rating)
                db.session.add(vote)
                db.session.commit()
                flash(user.username + ' successfully rated.', 'success')

        # Rating is not True or False; rating is invalid
        else:
            flash('Invalid rating.', 'warning')

        return redirect( url_for('main.profile', username = user.username) )

    else:
        flash('A user who does not exist cannot be rated.', 'info')
        abort(404)
