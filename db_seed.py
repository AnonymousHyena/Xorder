from db_setup import *
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///name.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

if __name__ == '__main__':
    session.query(Users).delete()
    session.query(Stores).delete()
    session.query(Items).delete()
     
    user = Users()
    user.name = 'Bob'
    user.password = 123
    user.mail = 'bob@bobland.com'
    session.add(user)

    store = Stores()
    store.name = 'Tropio'
    store.user_id = session.query(Users).filter_by(name='Bob').one().id
    session.add(store)

    item = Items()
    item.name = 'frappe'
    item.price = 2.5
    item.store_id = session.query(Stores).filter_by(name="Tropio").one().id

    session.add(item)



    session.commit()