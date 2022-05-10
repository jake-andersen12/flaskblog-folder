
from flask import Flask, escape, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager #importing the class LoginManager from flask_login

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bfca830ef51262833d66ffac439ead34'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) #password hashing algorithm
login_manager = LoginManager(app)  #This whole section is to initialize or make an instance of it. (app) it passes the app, into the class.
login_manager.login_view = 'login' #'login' is the function name for our route. The same that would be used in url_for
login_manager.login_message_category = 'info' #'info is a boostrap class which makes the login message look nice.

from flaskblog import routes