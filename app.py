from db_setup import *

from flask import Flask, request, render_template, redirect, url_for
from flask import session as login_session

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from views.users import blueprint as blueprint_users
from views.stores import blueprint as blueprint_stores
from views.items import blueprint as blueprint_items

from forms import LoginForm

engine = create_engine('sqlite:///xorder.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.register_blueprint(blueprint_users, url_prefix='/user')
app.register_blueprint(blueprint_stores, url_prefix='/store')
app.register_blueprint(blueprint_items, url_prefix='/store/<storeid>/item')

@app.route('/')
def index():
	if 'name' in login_session:
		return redirect(url_for('users.show'))
	return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def showLogin():
	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data
		try:
			dude = session.query(Users).filter_by(mail=email).one()
			if dude.password == form.password.data:
				login_session['name'] = dude.name
				login_session['email'] = dude.mail
				return redirect(url_for('users.show'))
			return render_template('login.html', form=form)
		except:
			return render_template('login.html',form=form,error='User not found')
	return render_template('login.html', form=form)
		
@app.route('/disconnect')
def disconnect():
	del login_session['name']
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(host = '0.0.0.0',port=5000)