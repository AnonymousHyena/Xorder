from db_setup import *

from flask import Flask, request, render_template, redirect, url_for
from flask import session as login_session

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from blues.users import blueprint as blueprint_users
from blues.stores import blueprint as blueprint_stores
from blues.items import blueprint as blueprint_items

engine = create_engine('sqlite:///name.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)
app.register_blueprint(blueprint_users, url_prefix='/user')
app.register_blueprint(blueprint_stores, url_prefix='/user/<userid>/store')
app.register_blueprint(blueprint_items, url_prefix='/user/<userid>/store/<storeid>/item')

@app.route('/')
def index():
	# session.rollback()
	# stre = session.query(Users).filter_by(name="Bob").one().stores[0]
	# items = session.query(Items).filter_by(store=stre).all()
	# return str(stre.id)
	return render_template('index.html')

@app.route('/login')
def login():
	pass

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0',port=5000)