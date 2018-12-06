from ..db_setup import *
from flask import Blueprint, request, render_template, redirect, url_for
from flask import session as login_session

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

from ..forms import RegisterShopForm

DBSession = sessionmaker(bind = engine)

blueprint = Blueprint('stores',__name__)

@blueprint.route('/show/<strid>')
def show(strid):
	session = DBSession()
	dude = session.query(Users).filter_by(mail=login_session['email']).one()
	store = session.query(Stores).filter_by(id=strid).one()
	if store in dude.stores:
		return render_template('Stores/show.html', str=store)
	return render_template('index.index')

@blueprint.route('/new', methods=['POST', 'GET'])
def new():
	form = RegisterShopForm()
	if form.validate_on_submit():
		session = DBSession()
		dude = session.query(Users).filter_by(mail=login_session['email']).one()
		store = Stores()
		store.name = form.name.data
		try:
			session.add(store)
			session.commit()
			dude.stores.append(store)
			session.commit()
			return redirect(url_for('index.index'))
		except exc.IntegrityError:
			session.rollback()
			return render_template('Stores/register.html', form=form, error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])
	return render_template('Stores/register.html', form=form)
