from flask import Flask, request, render_template, redirect, url_for
from flask import session as login_session

from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config.default')
app.config.from_pyfile('config.py')
app.config.from_envvar('APP_CONFIG_FILE')

bcrypt = Bcrypt(app)

from db_setup import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

DBSession = sessionmaker(bind = engine)

@login_manager.user_loader
def load_user(userid):
	session = DBSession()
	return session.query(Users).filter_by(id=userid).first()

from views.users import blueprint as blueprint_users
from views.stores import blueprint as blueprint_stores
from views.items import blueprint as blueprint_items
from views.index import blueprint as blueprint_index

app.register_blueprint(blueprint_index)
app.register_blueprint(blueprint_users, url_prefix='/user')
app.register_blueprint(blueprint_stores, url_prefix='/store')
app.register_blueprint(blueprint_items, url_prefix='/store/<storeid>/item')