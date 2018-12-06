# Standard Configuration for SQLAlchemy 
import sys
import os

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from flask_login import UserMixin

from . import bcrypt

Base = declarative_base()

# End of Standard Configuration

items_users = Table('items_users',Base.metadata,
	Column('item_id',Integer,ForeignKey('items.id')),
	Column('user_id',Integer,ForeignKey('users.id')),
	Column('table',Integer),
	Column('timestamp',Integer), #data type change to timestamp
	UniqueConstraint('timestamp', 'item_id', 'user_id', name='UC_timestamp_item_id_user_id'))

stores_users_waiters = Table('stores_users_waiters',Base.metadata,
	Column('store_id',Integer,ForeignKey('stores.id')),
	Column('user_id',Integer,ForeignKey('users.id')),
	UniqueConstraint('store_id', 'user_id', name='UC_store_id_user_id_waiter'))

stores_users_owners = Table('stores_users_owners',Base.metadata,
	Column('store_id',Integer,ForeignKey('stores.id')),
	Column('user_id',Integer,ForeignKey('users.id')),
	UniqueConstraint('store_id', 'user_id', name='UC_store_id_user_id_owner'))

class Users(Base, UserMixin):
	__tablename__ = 'users'

	id = Column(Integer, primary_key = True)
	name = Column(String(25), nullable = False)
	_password = Column(String(128), nullable = False)
	mail = Column(String(45), nullable = False, unique = True)
	mail_confirmed = Column(Boolean,nullable = False, default=False)
	orders = relationship("Items", secondary = items_users)
	admin = relationship("Stores", secondary = stores_users_waiters)
	stores = relationship("Stores", secondary = stores_users_owners)

	@hybrid_property
	def password(self):
		return self._password

	@password.setter
	def password(self, plaintext):
		self._password = bcrypt.generate_password_hash(plaintext)

	def is_correct_password(self,plaintext):
		return bcrypt.check_password_hash(self._password, plaintext)

class Stores(Base):
	__tablename__ = 'stores'

	id = Column(Integer, primary_key = True)
	name = Column(String(15), nullable = False)

	waiters = relationship(Users, secondary = stores_users_waiters)

class Items(Base):
	__tablename__ = 'items'

	id = Column(Integer, primary_key = True)
	name = Column(String(15), nullable = False)
	description = Column(String(15), nullable = True)
	price = Column(Float, nullable = False)
	store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)

	store = relationship(Stores, uselist=False)


engine = create_engine('sqlite:///xorder/xorder.db')

Base.metadata.create_all(engine)
