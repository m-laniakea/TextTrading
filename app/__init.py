from flask import Flask, render_template
from flask.ext.moment import Moment
from flask.ext.bootstrap import Bootstrap
from datetime import datetime


app = Flask(__name__)

moment = Moment(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template( 'index.html', current_time=datetime.utcnow() )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run()
