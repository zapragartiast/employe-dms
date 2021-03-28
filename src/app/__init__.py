import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app_settings = os.getenv(
    'APP_SETTINGS',
    'src.app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# avoid circular module import
from src.app.routes import auth_blueprint
app.register_blueprint(auth_blueprint)
