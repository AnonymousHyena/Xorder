# Standard Configuration for SQLAlchemy 
import sys
import os

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# End of Standard Configuration

items_users = Table('items_users',Base.metadata,
	Column('item_id',Integer,ForeignKey('items.id')),
	Column('user_id',Integer,ForeignKey('users.id')),
	Column('table',Integer),
	Column('timestamp',Integer), #data type change to timestamp
	UniqueConstraint('timestamp', 'item_id', 'user_id', name='UC_timestamp_item_id_user_id'))

class Users(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key = True)
	name = Column(String(15), nullable = False)
	password = Column(Integer, nullable = False)
	mail = Column(String(25), nullable = False)
	orders = relationship("Items", secondary = items_users)

class Stores(Base):
	__tablename__ = 'stores'

	id = Column(Integer, primary_key = True)
	name = Column(String(15), nullable = False)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

	owner = relationship(Users, uselist=False)


class Items(Base):
	__tablename__ = 'items'

	id = Column(Integer, primary_key = True)
	name = Column(String(15), nullable = False)
	description = Column(String(15), nullable = True)
	price = Column(Float, nullable = False)
	store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)

	store = relationship(Stores, uselist=False)


engine = create_engine('sqlite:///name.db')

Base.metadata.create_all(engine)
