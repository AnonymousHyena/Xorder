from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired ,Email

from util.validators import Unique

from db_setup import *

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])

class SignUpForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email(), 
		Unique(Users,Users.mail,'There is already an account with that email.')])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('ConfirmPassword', validators=[DataRequired()])

class RegisterShopForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
		