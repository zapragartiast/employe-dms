import unittest

from flask import current_app
from flask_testing import TestCase

from src.app import app
from src.app.config import PG_URI_DEV


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('src.app.config.DevelopmentConfig')
        return app
    
    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'kunci-rahasia')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == PG_URI_DEV
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('src.app.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'kunci-rahasia')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == PG_URI_DEV + '_test'
        )


if __name__ == '__main__':
    unittest.main()
