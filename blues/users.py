from db_setup import *
from flask import Blueprint, request, render_template, redirect, url_for
from flask import session as login_session

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, exc

engine = create_engine('sqlite:///xorder.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

blueprint = Blueprint('users',__name__)

@blueprint.route('/profile')
def show():
	return render_template('Users/show.html')

@blueprint.route('/new')
def new():
	return render_template('Users/form.html')

@blueprint.route('/create', methods=['POST'])
def create():
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
		login_session['name'] = name
		login_session['email'] = mail
		return redirect(url_for('users.show'))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Users/form.html', error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

@blueprint.route('/edit')
def edit():
	dude = session.query(Users).filter_by(mail=login_session['email']).one()
	return render_template('Users/form.html', usr=dude)

@blueprint.route('/update', methods=['POST'])
def update():
	dude = session.query(Users).filter_by(mail=login_session['email']).one()
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
		return render_template('Users/form.html', error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])
