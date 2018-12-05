from db_setup import *
from flask import Blueprint, request, render_template, redirect, url_for
from flask import session as login_session

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, exc

from forms import SignUpForm

engine = create_engine('sqlite:///xorder.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

blueprint = Blueprint('users',__name__)

@blueprint.route('/profile')
def show():
	stores = session.query(Users).filter_by(mail=login_session['email']).one().stores
	return render_template('Users/show.html', strs=stores)

@blueprint.route('/signup', methods=['POST', 'GET'])
def new():
	form = SignUpForm()
	if form.validate_on_submit():
		dude = Users()
		dude.name = form.name.data
		dude.mail = form.email.data
		dude.password = form.password.data
		try:
			session.add(dude)
			session.commit()
			login_session['name'] = form.name.data
			login_session['email'] = form.email.data
			return redirect(url_for('users.show'))
		except exc.IntegrityError:
			session.rollback()
			return render_template('Users/signup.html', form=form, error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])
	return render_template('Users/signup.html', form=form)