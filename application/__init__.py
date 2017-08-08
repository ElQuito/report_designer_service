import os
from flask import Flask
from config import basedir, connect_db
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_object('config')

connect_db_lite = SQLAlchemy(application)
from application import views
from application.models import model
from application.lib import ConvertToXml