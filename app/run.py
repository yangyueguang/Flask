# coding: utf-8
# @date: 2019-11-10
import os
import sys
from app.utility.appManager import *
from flask_script import Manager
import app.config as conf
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

app = create_app()


if __name__ == '__main__':
    app.run(port=8000, debug=True)
    # db = SQLAlchemy(app)
    # Migrate(app, db)


