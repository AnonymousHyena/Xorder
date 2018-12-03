from db_setup import *
from flask import Blueprint, request, render_template, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, exc

engine = create_engine('sqlite:///xorder.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

blueprint = Blueprint('stores',__name__)

@blueprint.route('/new')
def new(userid):
	return render_template('Stores/form.html', usr=userid)

@blueprint.route('/create', methods=['POST'])
def create(userid):
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

@blueprint.route('/edit/<strid>')
def edit(userid, strid):
	stre = session.query(Users).filter_by(id=strid).one()
	return render_template('Stores/form.html', usr=userid, store=stre)

@blueprint.route('/update/<strid>', methods=['POST'])
def update(userid, strid):
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
