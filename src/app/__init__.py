import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    __name__,
    static_url_path='',
    static_folder='upload'
    )

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'upload/files')


app_settings = os.getenv(
    'APP_SETTINGS',
    'src.app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)


bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# avoid circular module import
from .routes import api_blueprint
app.register_blueprint(api_blueprint)
