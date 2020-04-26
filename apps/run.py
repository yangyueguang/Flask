# coding: utf-8
# @date: 2019-11-10
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)

from apps.utility.appManager import *
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

app = create_app(os.environ.get('ENV', 'default'))


if __name__ == '__main__':

    # app = create_app(os.environ.get('ENV', 'default'))
    manage = Manager(app)
    db = SQLAlchemy(app)
    Migrate(app, db)
    manage.add_command("db", MigrateCommand)

    # app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/0'
    # app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/0'
    # celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    # # celery = Celery(app.name, broker='redis://', backend='redis://', include=['LogHandler.run'])
    # celery.conf.update(app.config)
    #
    # @celery.task(name='task')
    # def start_logs_upload_task():
    #     print('hello=========')
    #     log_task = LogHandler()
    #     log_task.run()
    # start_logs_upload_task.apply_async()
    # task = celery.send_task('task', args=[], kwargs={})

    manage.run()


