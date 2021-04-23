import os
import unittest
import coverage

from flask_script import Manager, Command, Option
from flask_migrate import Migrate, MigrateCommand
from src.app import app, db


class GunicornServer(Command):
    """Run the app with gunicorn server"""
    def __init__(self, host='0.0.0.0', port=80, workers=2, timeout=0):
        self.host = host
        self.port = port
        self.workers = workers
        self.timeout = timeout

    def get_options(self):
        return (
            Option('-H', '--host',
                   dest='host',
                   default=self.host),
            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),
            Option('-w', '--workers',
                   dest='workers',
                   type=int,
                   default=self.workers),
            Option('-t', '--timeout',
                   dest='timeout',
                   type=int,
                   default=self.timeout)
        )

    def __call__(self, app, host, port, workers, timeout):
        from gunicorn import version_info
        if version_info < (0, 9, 0):
            from gunicorn.arbiter import Arbiter
            from gunicorn.config import Config
            arbiter = Arbiter(Config(
                {'bind': '%s:%d' % (host, int(port)), 'workers': workers}
            ), app)
            arbiter.run()
        else:
            from gunicorn.app.base import Application

            class FlaskApplication(Application):
                def init(self, parser, opts, args):
                    return {
                        'bind': '{0}:{1}'.format(host, port)
                    }

                def load(self):
                    return app
            FlaskApplication().run()


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

# start gunicorn server
manager.add_command('gunicorn', GunicornServer())


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
