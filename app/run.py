# coding: utf-8
# @date: 2019-11-10
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.utility.appManager import *
from flask_script import Manager
import app.config as conf
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

app = create_app()


if __name__ == '__main__':
    app.run()
    print(BASE_DIR)
    print('WORKERS: {}'.format(conf.workers))
    print('THREADS: {}'.format(conf.threads))
    # # db = SQLAlchemy(app)
    # # Migrate(app, db)


