import os
import pyodbc
import urllib

basedir = os.path.abspath(os.path.dirname(__file__))

conDEBUG_connect = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=ADP_transport;Trusted_Connection=yes;'
#conDEBUG = urllib.parse.quote_plus(conDEBUG_connect)

#подключение к базе для загрузки настроек по одчёту
#SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc:///?odbc_connect=%s' % conDEBUG
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'settings.db') + '?check_same_thread=False'
SQLALCHEMY_TRACK_MODIFICATIONS = True
#SQLALCHEMY_POOL_SIZE = 20

#подключение к базе для выполнения кранимых процедур
connect_db = pyodbc.connect(conDEBUG_connect)

CSRF_ENABLED = True

SECRET_KEY = 'you-will-never-guess'