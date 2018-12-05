from wtforms.validators import ValidationError
from db_setup import *

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///xorder.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class Unique(object):
	def __init__(self, model, field, message=u'This element already exists.'):
		self.model = model
		self.field = field
		self.message = message

	def __call__(self, form, field):
		check = session.query(self.model).filter(self.field==field.data).first()
		if check:
			raise ValidationError(self.message)
