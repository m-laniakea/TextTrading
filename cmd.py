## High-level control module
#  

import os
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

def shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=shell_context))

if __name__ == '__main__':
    manager.run()


    


