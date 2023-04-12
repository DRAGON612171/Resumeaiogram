from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from Resumeaiogram.config import Config

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager()

from Resumeaiogram.app import routes