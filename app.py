##
# This is the main program for our website
#
# Launch this application in Python virtual environment 7.2 for proper 
# functionality.  Prerequisites include:
#     dominate==2.1.16
#     Flask==0.10.1
#     Flask-Bootstrap==3.3.5.7
#     Flask-Moment==0.5.1
#     Flask-Script==2.0.5
#     itsdangerous==0.24
#     Jinja2==2.8
#     MarkupSafe==0.23
#     visitor==0.1.2
#     Werkzeug==0.11.3
#     wheel==0.26.0
#
# @author eir; Ruby Kassalla; Erik Greif; Cate Yochum; Bruce Harr;
#         Erick Ngo; Aaron Gupta;
# @date   2016.01.30
##

from flask import Flask, render_template
from flask.ext.moment import Moment
from flask.ext.bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)


moment = Moment(app)
bootstrap = Bootstrap(app)


## 
# This is the index page (homepage)
# Here the user will be shown all of the initial content
##
@app.route('/')
def index():
    return render_template( 'index.html', current_time=datetime.utcnow() )


##
# This page will be loaded when the server fails to find a requested page
##
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


##
# This is the main program
# Here the code for starting up the program is run
##
if __name__ == '__main__':
    app.run()
