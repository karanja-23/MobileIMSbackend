from flask import Flask
from models import db
import os
from flask_migrate import Migrate
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
db.init_app(app)
migrate = Migrate(app, db)