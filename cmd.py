#!/usr/bin/env python

## 
# High-level control module
#
# Usage hints: "./cmd.py <command> --help"
# or      "python cmd.py <command> --help"
#
# Launch this application in Python virtual environment 2.7 for proper 
# functionality.  
#
# Currently this application depends on ** sqlite **
#
# Dependencies are to be installed with:
#		pip install -r reqs.txt
#
# @author eir; Ruby Kassalla; Erik Greif; Cate Yochum; Bruce Harr;
#         Erick Ngo; Aaron Gupta;
# @date   2016.01.30
##

import os
from app import create_app, db
from app.models import User, Book, Conversation, Message, Vote
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Shell

# Create app using default configuration from cfg.py
app = create_app('default')

# Set up migrate for db operations
migrate = Migrate(app, db)

# Set up CLI interface
manager = Manager(app)

def shell_context():
    return dict(app=app, db=db, Book=Book, User=User, Conversation=Conversation, Message=Message, Vote=Vote)


# Define CLI commands
manager.add_command("shell", Shell(make_context=shell_context))
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()


    


