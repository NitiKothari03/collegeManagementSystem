from flask import Flask
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
import warnings

app = Flask(__name__)

app.secret_key = '3w4e6t7by8nh9jm0kbvufjifi4'

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

app.config['SQLALCHEMY_ECHO'] = True

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root:root@localhost:3306/projectdb'

app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

db = SQLAlchemy(app)

from base.com import controller
