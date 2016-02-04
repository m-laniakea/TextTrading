##
# Database definitions for SQLAlchemy
##

from . import db
from flask.ext.login import UserMixin
from . import login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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
    books = db.relationship("Book", backref="owner")
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

    @staticmethod
    def populate():
        db.create_all()

        emails = ["Bruce@uw.edu", "Cate@uw.edu", "m-laniakea@uw.edu", "erick@uw.edu", "BitFracture@uw.edu", "Ruby@uw.edu"]
        unames = ["Bruce", "Cate", "m-laniakea", "erickgnoUW", "BitFracture", "Ruby"]

        for i in range(len(emails)):
            user = User(email=emails[i], username=unames[i], set_password = 'flipthetable')
            db.session.add(user)
        
        db.session.commit()

##
# Books have:
# *one owner (Parent)
##
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=False, index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))




