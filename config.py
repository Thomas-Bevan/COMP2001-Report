import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import urllib.parse

import pyodbc

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

server = 'dist-6-505.uopnet.plymouth.ac.uk'
database = 'COMP2001_TBevan'
username = 'TBevan'
password = 'XcbV225+'
driver = '{ODBC Driver 17 for SQL Server}'

app = connex_app.app

app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mssql+pyodbc://TBevan:XcbV225+@dist-6-505.uopnet.plymouth.ac.uk/COMP2001_TBevan"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&Encrypt=yes"
    "&TrustServerCertificate=yes"
    "&Trusted_Connection=No"
)



app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



db = SQLAlchemy(app)
ma = Marshmallow(app)
