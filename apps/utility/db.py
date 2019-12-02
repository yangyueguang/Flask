# coding: utf-8
# @date: 2019-11-10
# @author: xuechao@datagrand.com
import os
import redis
from flask import _app_ctx_stack, current_app
from sqlalchemy import create_engine, orm
from sqlalchemy_utils.functions import database_exists, create_database, drop_database
from apps.models import Base
import apps.config

isOpen = 1 #0关闭1开启
engine = create_engine(apps.config.SQLALCHEMY_DATABASE_URI)
DBSession = orm.sessionmaker(bind=engine, autocommit=False, autoflush=False)
session = DBSession()


class ScopedSession(orm.scoped_session):
    def __init__(self, app=None):
        super(ScopedSession, self).__init__(DBSession, scopefunc=_app_ctx_stack.__ident_func__)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.scoped_session = self

        @app.teardown_appcontext
        def remove_scoped_session(*args, **kwargs):
            app.scoped_session.remove()


def _get_session():
    app = current_app._get_current_object()
    if not hasattr(app, "scoped_session"):
        raise AttributeError("{0} has no 'scoped_session' attribute. You need to initialize it with a ScopedSession.".format(app))
    return app.scoped_session


def create_all_tables():
    Base.metadata.create_all(engine)
    session.commit()


def create_tables(*models):
    """
    pass models list or tuple, eg: models=(User, Role, ...)
    """
    for model in models:
        model.__table__.create(engine)


def drop_tables(*models):
    """
    pass models list or tuple, eg: models=(User, Role, ...)
    """
    for model in models:
        try:
            model.__table__.drop(engine)
        except:
            if os.environ.get('ENV') == 'product':
                raise
            else:
                continue


def session_commit():
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def session_flush():
    try:
        session.flush()
    except Exception as e:
        session.rollback()
        raise e


def init_database_tables(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = apps.config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_BINDS'] = None
    if not database_exists(apps.config.SQLALCHEMY_DATABASE_URI):
        create_database(apps.config.SQLALCHEMY_DATABASE_URI)
    create_all_tables()


def reinit_database_tables():
    if database_exists(apps.config.SQLALCHEMY_DATABASE_URI):
        drop_database(apps.config.SQLALCHEMY_DATABASE_URI)
    create_database(apps.config.SQLALCHEMY_DATABASE_URI)
    create_all_tables()


def connect_redis():
    try:
        rdb = redis.StrictRedis(
            host="127.0.0.1",
            port=6379,
            db=1,
            password='')
        return rdb
    except Exception as e:
        print(e.message)