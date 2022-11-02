from flask import Flask, Blueprint

from config import Config
from github_config import *
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restx import Api
import os

app = Flask(__name__)
app.config.from_object(Config)
logger = app.logger
logger.setLevel(app.config['LOGGER_LEVEL'])
db = SQLAlchemy(app)
session = db.session

app.secret_key = os.urandom(24)


# BLUEPRINTS
# https://flask.palletsprojects.com/en/2.2.x/blueprints/
blueprint = Blueprint('api', __name__, url_prefix="/api/v1")
api = Api(blueprint, version='1.2', title="COMPETITION API", description="COMPETITION API")
app.register_blueprint(blueprint)
CORS(app, headers='Content-Type', allow_headers='*', origins='*')

from .models import *
from .service import *
from .routes import *
