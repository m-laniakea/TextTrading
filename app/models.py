##
# Database definitions for SQLAlchemy
##

from . import db
from flask.ext.login import UserMixin
from . import login_manager 
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import random, os
from random import randint

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
##
# Users have:
# *one role_id 
# *many books
#
##  UserMixin provides:
#
#   is_authenticated()
#   is_anonymous()
#
#   get_id()    # Return user identifier 
##

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    books = db.relationship("Book", backref="owner", lazy="dynamic")
    user_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_online = db.Column(db.DateTime(), default=datetime.utcnow) 
    rating = db.Column(db.Float(precision=3), default = 0)
    ratings_count = db.Column(db.Integer, default = 0)

    @property
    def password(self):
        raise AttributeError('Unreadable Attribute')

    @password.setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    ##
    # Initiate & Populate db with users,
    # randomly generated book titles
    #
    # Requires dct.txt dictionary
    ##
    @staticmethod
    def populate():
        # Initialize db with models from this file
        db.create_all()
        basedir = os.path.abspath(os.path.dirname(__file__))
        wordlist = [l.strip() for l in open(os.path.join(basedir, "dct.txt"))]

        emails = ["Bruce@uw.edu", "Cate@uw.edu", "m-laniakea@uw.edu", "erick@uw.edu", "BitFracture@uw.edu", "Ruby@uw.edu"]
        unames = ["Bruce", "Cate", "m-laniakea", "erickgnoUW", "BitFracture", "Ruby"]

        ## Populate db with user in the two lists, assign random rating
        for i in range(len(emails)):
            # Biased-Random integer to determine rating
            tmp = 0 if randint(0,6) < 3 else randint(1000, 5000)

            user = User(email = emails[i], username = unames[i], set_password = 'ftt',
                    rating = tmp/1000.0, ratings_count = 0 if (tmp == 0) else randint(1, 88) )
            db.session.add(user)

            ## Gen fake books with random names, titles, prices, & conditions
            for j in range( randint(2, 8) ):
                book = Book(title = User.gen_placeholder(wordlist, randint(1,3)), owner=user, author = User.gen_placeholder(wordlist, 2),
                        price = 0 if (randint(0,2) == 0 ) else randint(0,8888)/100.0, condition = randint(1,5))
                db.session.add(book)
        
        db.session.commit()

    @staticmethod
    def gen_placeholder(words, n):
        title = ""
        
        if n > 0:
            for i in range(n - 1): 
                title += random.choice(words).title() + " "
            title += random.choice(words).title() 

        return title

    ##
    # END POPULATE
    ##

##
# Books have:
# *one owner (Parent)
##
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=False, index=True)
    author = db.Column(db.String(128), unique=False, index=True)
    condition = db.Column(db.Integer, unique=False, index=True)
    price = db.Column(db.Float(precision=2, default=0))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))




