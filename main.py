import os
import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.app import app, db

APP_COVERAGE = coverage.coverage(
    branch=True,
    include='src/*',
    omit=[
        'src/app/config.py',
        'src/tests/*',
        'src/app/*/__init__.py',
        'src/app/api/*/__init__.py*'
    ]
)
APP_COVERAGE.start()

manager = Manager(app)
migrate = Migrate(app, db, compare_type=True)

# do migration
manager.add_command('migrasi', MigrateCommand)


@manager.command
def test():
    """Run unit test without coverage"""
    tests = unittest.TestLoader().discover('src/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def test_cov():
    """Run unit test with coverage"""
    tests = unittest.TestLoader().discover('src/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=3).run(tests)
    if result.wasSuccessful():
        APP_COVERAGE.stop()
        APP_COVERAGE.save()
        print('Coverage Summary:')
        APP_COVERAGE.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        cov_dir = os.path.join(basedir, 'tmp/coverage')
        APP_COVERAGE.html_report(directory=cov_dir)
        print('HTML Version: file://%s/index.html' % cov_dir)
        APP_COVERAGE.erase()
        return 0
    return 1


@manager.command
def buat_db():
    """Buat database"""
    db.create_all()


if __name__ == '__main__':
    manager.run()
