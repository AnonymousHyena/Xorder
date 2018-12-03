from db_setup import *
from flask import Blueprint, request, render_template, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, exc

engine = create_engine('sqlite:///xorder.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

blueprint = Blueprint('items',__name__)

@blueprint.route('/new')
def new(userid,storeid):
	items = session.query(Items).filter_by(store_id=storeid).all()
	return render_template('Items/form.html', user=userid ,store=storeid, itm=items)

@blueprint.route('/create', methods=['POST'])
def create(userid,storeid):
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

@blueprint.route('/edit/<itemid>')
def edit(userid,storeid,itemid):
	thing = session.query(Items).filter_by(id=itemid).one()
	return render_template('Items/form.html', usr=userid, store=storeid, item=thing)

@blueprint.route('/update/<itemid>', methods=['POST'])
def update(userid,storeid,itemid):
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
