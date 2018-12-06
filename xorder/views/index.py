from ..db_setup import *
from flask import Blueprint, request, render_template, redirect, url_for

from flask_login import current_user


from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

blueprint = Blueprint('index',__name__)

@blueprint.route('/')
def index():
	if current_user.is_authenticated:
		return redirect(url_for('users.show'))
	return render_template('index.html')