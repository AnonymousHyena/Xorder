from ..db_setup import *
from flask import Blueprint, request, render_template, redirect, url_for

from flask_login import login_required, current_user

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

from ..forms import RegisterShopForm

DBSession = sessionmaker(bind = engine)

blueprint = Blueprint('stores',__name__)

@blueprint.route('/show/<strid>')
@login_required
def show(strid):
	session = DBSession()
	store = session.query(Stores).filter_by(id=strid).one()
	if store in current_user.stores:
		return render_template('Stores/show.html', str=store)
	return render_template('index.index')

@blueprint.route('/new', methods=['POST', 'GET'])
@login_required
def new():
	form = RegisterShopForm()
	if form.validate_on_submit():
		session = DBSession()
		store = Stores()
		store.name = form.name.data
		try:
			session.add(store)
			session.commit()
			current_user.stores.append(store)
			session.commit()
			return redirect(url_for('index.index'))
		except exc.IntegrityError:
			session.rollback()
			return render_template('Stores/register.html', form=form, error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])
	return render_template('Stores/register.html', form=form)
