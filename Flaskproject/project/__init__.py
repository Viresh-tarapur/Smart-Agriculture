
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager, login_user
from flask_migrate import Migrate  
import serial
import pynmea2




app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SECRET_KEY'] = '6e8d2fcb509f785bae4734ab'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'user_session'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login_page'
migrate = Migrate(app, db)

from project import routes
from project.models import User
from project.models import BinStatus
from project.models import BinLocation


    


