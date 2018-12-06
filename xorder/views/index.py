from ..db_setup import *
from flask import Blueprint, request, render_template, redirect, url_for
from flask import session as login_session

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

blueprint = Blueprint('index',__name__)

@blueprint.route('/')
def index():
	if 'name' in login_session:
		return redirect(url_for('users.show'))
	return render_template('index.html')