from ..db_setup import *
from flask import Blueprint, request, render_template, redirect, url_for
from flask import session as login_session

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

from ..forms import SignUpForm, LoginForm
from ..util.security import ts, send_email

DBSession = sessionmaker(bind = engine)

blueprint = Blueprint('users',__name__)

@blueprint.route('/profile')
def show():
	session = DBSession()
	stores = session.query(Users).filter_by(mail=login_session['email']).one().stores
	return render_template('Users/show.html', strs=stores)

@blueprint.route('/login', methods=['POST', 'GET'])
def showLogin():
	form = LoginForm()
	if form.validate_on_submit():
		session = DBSession()
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
		
@blueprint.route('/disconnect')
def disconnect():
	del login_session['name']
	return redirect(url_for('index.index'))

@blueprint.route('/signup', methods=['POST', 'GET'])
def new():
	form = SignUpForm()
	if form.validate_on_submit():
		session = DBSession()
		dude = Users()
		dude.name = form.name.data
		dude.mail = form.email.data
		dude.password = form.password.data
		try:
			session.add(dude)
			session.commit()
			login_session['name'] = form.name.data
			login_session['email'] = form.email.data

			subject = 'Confirm your email'
			token = ts.dumps(form.email.data, salt='email-confirm-key')

			confirm_url = url_for(
				'users.confirm_mail',
				token=token,
				_external=True)

			html = render_template(
				'email/activate.html',
				confirm_url=confirm_url)

			#send_email(form.email.data,subject,html)
			#confiramtion mail feature disabled for practivcal reasons but functional

			return redirect(url_for('users.show'))
		except exc.IntegrityError:
			session.rollback()
			return render_template('Users/signup.html', form=form, error=str(sys.exc_info()[1]).split(") ")[1].split(" [")[0])
	return render_template('Users/signup.html', form=form)

@blueprint.route('/confirm/<token>')
def confirm_mail(token):
	try:
		email = ts.load(token, salt='email-confirm-key', max_age=86400)
	except:
		return redirect(url_for('users.login'))

	session = DBSession()

	user = session.query(Users).filter_by(mail=email).one()
	user.confirm_mail = True

	session.commit()
	return redirect(url_for('users.login'))