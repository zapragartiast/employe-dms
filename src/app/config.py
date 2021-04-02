import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# database env
load_dotenv()
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASS = os.getenv('DATABASE_PASS')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')

# database endpoint
PG_URI_DEV = 'postgresql://' + DATABASE_USER + ':' + DATABASE_PASS + '@' + DATABASE_HOST + '/' + DATABASE_NAME
PG_URI_PROD = 'postgresql://' + DATABASE_USER + ':' + DATABASE_PASS + '@' + DATABASE_HOST + '/' + DATABASE_NAME

UPLOAD_FOLDER = os.path.join(basedir, 'upload/files')


class BaseConfig:
    """Base Configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


class DevelopmentConfig(BaseConfig):
    """Development Configuration"""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 10
    SQLALCHEMY_DATABASE_URI = PG_URI_DEV


class TestingConfig(BaseConfig):
    """Testing Configuration"""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = PG_URI_DEV + "_test"
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.getenv('PROD_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = PG_URI_PROD
