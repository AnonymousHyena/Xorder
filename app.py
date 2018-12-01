from db_setup import *
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from flask import session as login_session
#from flask_uploads import UploadSet, configure_uploads, IMAGES
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, exc

import os
import random
import string

engine = create_engine('sqlite:///name.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
def index():
	usr = session.query(Users).all()
	return str(session.query(Stores).filter_by(name="Tropio").one().waiters[0].id)

@app.route('/user/new')
def newUser():
	return render_template('Users/form.html')

@app.route('/user/create', methods=['POST'])
def createUser():
	usr = Users()
	name = format(request.form['name'])
	mail = format(request.form['email'])
	password = format(request.form['password'])
	if name!="":
		usr.name=name
	if mail!="":
		usr.mail=mail
	if password!="":
		usr.password=password
	try:
		session.add(usr)
		session.commit()
		return redirect(url_for('index'))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Users/form.html', error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

@app.route('/user/edit/<usrid>')
def editUser(usrid):
	dude = session.query(Users).filter_by(id=usrid).one()
	return render_template('Users/form.html', usr=dude)

@app.route('/user/update/<usrid>', methods=['POST'])
def updateUser(usrid):
	dude = session.query(Users).filter_by(id=usrid).one()
	name = format(request.form['name'])
	mail = format(request.form['email'])
	password = format(request.form['password'])
	if name!="":
		dude.name=name
	if mail!="":
		dude.mail=mail
	if password!="":
		dude.password=password
	try:
		session.commit()
		return redirect(url_for('index'))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Users/form.html', usr=dude, error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

# @app.route('/store/new')
# def newStore():
# 	return render_template('Stores/form.html')

# @app.route('/store/create', methods=['POST'])
# def createStore():
# 	store = Store()
# 	name = format(request.form['name'])
# 	if name!="":
# 		store.name=name
# 	try:
# 		session.add(store)
# 		session.commit()
# 		return redirect(url_for('index'))
# 	except exc.IntegrityError:
# 		session.rollback()
# 		return render_template('Stores/form.html', error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

# @app.route('/store/edit/<strid>')
# def editStore(strid):
# 	dude = session.query(Users).filter_by(id=usr).one()
# 	return render_template('Users/form.html', us=dude)

# @app.route('/store/update/<usr>', methods=['POST'])
# def updateStore(usr):
# 	us = session.query(Attribute).filter_by(id=usr).one()
# 	name = format(request.form['name'])
# 	mail = format(request.form['email'])
# 	password = format(request.form['password'])
# 	if name!="":
# 		us.name=name
# 	if mail!="":
# 		us.mail=mail
# 	if password!="":
# 		us.password=password
# 	try:
# 		session.commit()
# 		return redirect(url_for('index'))
# 	except exc.IntegrityError:
# 		session.rollback()
# 		return render_template('Users/form.html', at=at, error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0',port=5000)