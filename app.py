from db_setup import *
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from flask import session as login_session
from flask_uploads import UploadSet, configure_uploads, IMAGES
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, exc

import os
import random
import string

engine = create_engine('sqlite:///name.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
def index():
	store = session.query(Stores).all()
	return store[0].owner.name

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0',port=5000)