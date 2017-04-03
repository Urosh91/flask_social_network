from flask import Flask, g
from flask_login import LoginManager

import models

DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.secret_key = 'nfgd90495u3fds0(%*85#%**()%&$fsd9463h()F&U$h'

login_manager = LoginManager()
login_manager.init_app(app)
# Setting up the login manager for app, paying attention to views, controlling user, etc.
login_manager.login_view = 'login'
# If user is not logged in this will redirect them to login view

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
        # gets users id that matches userid sent in the function and then returns it
    except models.DoesNotExist:
        # DoesNotExists comes from peewee, but considering it was imported in models it is possible to reference it
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.db
    g.db.connect()
    # g is a global object that can be used to set up things I want to have available everywhere


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


if __name__ == '__main__':
    models.initialize()
    models.User.create_user(
        username = 'Uros91',
        email= 'urosh43@gmail.com',
        password= 'password',
        admin=True
    )
    # make sure it's create_user and not default create, so the password will be hashed
    app.run(debug=DEBUG, host=HOST, port=PORT)