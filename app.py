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
	stre = session.query(Users).filter_by(name="Bob").one().stores[0]
	items = session.query(Items).filter_by(store=stre).all()
	return str(items[0].name)

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

@app.route('/user/<userid>/store/new')
def newStore(userid):
	return render_template('Stores/form.html', usr=userid)

@app.route('/user/<userid>/store/create', methods=['POST'])
def createStore(userid):
	store = Stores()
	name = format(request.form['name'])
	if name!="":
		store.name=name
	try:
		session.add(store)
		session.commit()
		usr = session.query(Users).filter_by(id=userid).one()
		usr.stores.append(store)
		session.commit()
		return redirect(url_for('index'))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Stores/form.html', usr=userid,error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

@app.route('/user/<userid>/store/edit/<strid>')
def editStore(userid, strid):
	stre = session.query(Users).filter_by(id=strid).one()
	return render_template('Stores/form.html', usr=userid, store=stre)

@app.route('/user/<userid>/store/update/<strid>', methods=['POST'])
def updateStore(userid, strid):
	stre = session.query(Stores).filter_by(id=strid).one()
	name = format(request.form['name'])
	if name!="":
		stre.name=name
	try:
		session.commit()
		return redirect(url_for('index'))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Stores/form.html', usr=userid, store=stre, error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

@app.route('/user/<userid>/store/<storeid>/item/new')
def newItem(userid,storeid):
	return render_template('Items/form.html', user=userid ,store=storeid)

@app.route('/user/<userid>/store/<storeid>/item/create', methods=['POST'])
def createItem(userid,storeid):
	item = Items()
	name = format(request.form['name'])
	description = format(request.form['description'])
	price = format(request.form['price'])
	if name!="":
		item.name=name
	if description!="":
		item.description=description
	if price!="":
		item.price=price
	item.store_id = storeid
	try:
		session.add(item)
		session.commit()
		return redirect(url_for('index'))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Items/form.html', user=userid ,store=storeid, error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

@app.route('/user/<userid>/store/<storeid>/item/edit/<itemid>')
def editItem(userid,storeid,itemid):
	thing = session.query(Items).filter_by(id=itemid).one()
	return render_template('Items/form.html', usr=userid, store=storeid, item=thing)

@app.route('/user/<userid>/store/<storeid>/item/update/<itemid>', methods=['POST'])
def updateItem(userid,storeid,itemid):
	thing = session.query(Items).filter_by(id=itemid).one()
	name = format(request.form['name'])
	description = format(request.form['description'])
	price = format(request.form['price'])
	if name!="":
		thing.name=name
	if description!="":
		thing.description=description
	if price!="":
		thing.price=price
	try:
		session.commit()
		return redirect(url_for('index'))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Items/form.html', usr=userid, store=storeid, item=thing, error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0',port=5000)