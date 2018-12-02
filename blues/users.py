from db_setup import *
from flask import Blueprint, request, render_template, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///xorder.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

blueprint = Blueprint('users',__name__)

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
		return redirect(url_for('index'))
	except exc.IntegrityError:
		session.rollback()
		return render_template('Users/form.html', error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])

@blueprint.route('/edit/<usrid>')
def edit(usrid):
	dude = session.query(Users).filter_by(id=usrid).one()
	return render_template('Users/form.html', usr=dude)

@blueprint.route('/update/<usrid>', methods=['POST'])
def update(usrid):
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
