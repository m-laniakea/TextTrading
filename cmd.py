## 
# High-level control module
#
# This is the main program for our website
#
# Launch this application in Python virtual environment 2.7 for proper 
# functionality.  
#
# Dependencies are to be installed with
#
#		pip install -r reqs.txt
#
#
# @author eir; Ruby Kassalla; Erik Greif; Cate Yochum; Bruce Harr;
#         Erick Ngo; Aaron Gupta;
# @date   2016.01.30
##

import os
from app import create_app, db
from app.models import User, Role, Book
from flask.ext.script import Manager, Shell


app = create_app('default')
manager = Manager(app)

def shell_context():
    return dict(app=app, db=db, Book=Book, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=shell_context))


if __name__ == '__main__':
    manager.run()


    


