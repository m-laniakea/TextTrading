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

##
# Table relating users and conversations
##
relations_table = db.Table('conversations_users', db.Model.metadata,
        db.Column('conversation_id', db.Integer, db.ForeignKey('conversations.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

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

    # Back-reference to multiple books the user will have
    books = db.relationship("Book", backref="owner", lazy="dynamic")
    user_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_online = db.Column(db.DateTime(), default=datetime.utcnow) 
    rating = db.Column(db.Float(precision=3), default = 0.0)
    ratings_count = db.Column(db.Integer, default = 0)
    conversations = db.relationship("Conversation", back_populates="participants", secondary=relations_table)

    @property
    def password(self):
        raise AttributeError('Unreadable Attribute')

    @password.setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Define default representation of User
    def __repr__(self):
        return 'User %s "%s", rating: %s' % (self.username, self.email, str(self.rating))

    ##
    #
    ## POPULATE
    #
    # Initiate & Populate db with users,
    # randomly generated book titles
    #
    # Requires dct.txt dictionary
    ##
    @staticmethod
    def populate():
        # Initialize db with models from this file
        db.create_all()
        print('Database initiation: \033[92mSuccess.\033[0m')

        # Get base directory for cross-system filepaths
        basedir = os.path.abspath(os.path.dirname(__file__))
        wordlist = [l.strip() for l in open(os.path.join(basedir, "dct.txt"))]

        emails = ["bruce@uw.edu", "cate@uw.edu", "m-laniakea@uw.edu", "erick@uw.edu", "bitfracture@uw.edu", "ruby@uw.edu"]
        unames = ["Bruce", "Cate", "m-laniakea", "erickgnoUW", "BitFracture", "Ruby"]

        ## Populate db with user in the two lists, assign random rating
        for i in range(len(emails)):
            # Biased-Random integer to determine rating
            tmp = 0 if randint(0,6) < 3 else randint(1000, 5000)

            user = User(email = emails[i], username = unames[i], set_password = 'ftt',
                    rating = tmp/1000.0, ratings_count = 0 if (tmp == 0) else randint(1, 88) )
            db.session.add(user)

            ## Gen fake books with random names, 
            ## titles, prices, ISBNs, & conditions
            for j in range( randint(2, 8) ):
                book = Book(title = User.gen_placeholder(wordlist, randint(1,3)), owner=user, 
                        author = User.gen_placeholder(wordlist, 2), isbn = randint(0,9999999999999),
                        price = 0 if (randint(0,2) == 0 ) else randint(0,8888)/100.0, condition = randint(1,5))
                db.session.add(book)
        
        db.session.commit()
        print('Database population: \033[92mSuccess.\033[0m')

    # Return 1-n random words as a string
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
    isbn = db.Column(db.Integer, unique=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return "\"%s\" by %s" % (self.title, self.author) 

##
# Conversations have:
# *two User as participants (Children) 
# *many messages
##
class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    participants = db.relationship("User", back_populates="conversations", secondary=relations_table)
    subject = db.Column(db.String(128))
    start_time = db.Column(db.DateTime(), default=datetime.utcnow)
    messages = db.relationship("Message", backref="conversation", lazy="dynamic")

    def __repr__(self):
        return 'Topic \"%s\" with %s & %s' % (self.subject, self.participants[0], self.participants[1])

##
# Messages have:
# *One conversation as parent
##
class Message(db.Model):
    __tablename__= 'messages'
    id = db.Column(db.Integer, primary_key=True)
    send_time = db.Column(db.DateTime(), default=datetime.utcnow)
    sender = db.Column(db.String(64))
    contents = db.Column(db.String(256)) 
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))

    # Define default representation
    def __repr__(self):
        return "%s : %s" % (self.sender, self.contents)
