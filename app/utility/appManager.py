# coding: utf-8
# @date: 2019-11-10
from flask import Flask
import threading
from flask import jsonify
from app.models import *
# import app.utility.db as db
from app.core import routes
from flask_cors import CORS
import app.config as st
# from app.utility import redis_db
from app.utility.dlog import dlog


def create_app():
    dlog('--start to run logs upload server--')
    flask_app = Flask(__name__, template_folder='data/static')
    # redis_db.connect_redis()
    load_conf(flask_app)
    # 跨域请求设置
    CORS(flask_app)
    # db.init_database_tables(flask_app)
    register_handlers(flask_app)
    # register_endpoints(flask_app)
    register_routes(flask_app)
    # register_plugins(flask_app)
    return flask_app


def register_handlers(flask_app):
    @flask_app.errorhandler(500)
    def server_error_handler(e):
        message = str(e)
        return jsonify({
            'code': 500,
            'message': message
        }), 500

    @flask_app.errorhandler(404)
    def not_found_handler(e):
        message = str(e)
        return jsonify({
            'code': 404,
            'message': message
        }), 404


def register_endpoints(flask_app):
    """
    注册所有的路由端点,蓝图
    """
    from app.services import apptest
    flask_app.register_blueprint(apptest, url_prefix='')


def register_routes(flask_app):
    """
    注册所有的路由端点
    """
    routes.add_routes(flask_app)


# def register_plugins(flask_app):
#     db.ScopedSession(flask_app) if db.isOpen == 1 else ""


def load_conf(app):
    app.debug = st.IS_DEBUG
    app.config['ROOT_DIR'] = '.'
    app.config['BASE_DIR'] = '.'
    app.config['TZ'] = 'Asia/Shanghai'
    # app.config['DEBUG'] = settings.HTTP_SERVER_LISTEN_IS_DEBUG
    # app.config['PORT'] = settings.HTTP_SERVER_LISTEN_PORT
    # mysql config
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@127.0.0.1:3306/super'
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 10,
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 1
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 30
    app.config["SECRET_KEY"] = "secret$%^&*key!@#$%^774ST$%^&*(you#!!@%never!@#$%^&guess"
    app.config["JWT_SECRET_KEY"] = "secret$%^&*key!@#$%^774@@$%^&*(you#!!@%never!@#$%^&guess"

    app.config["BCRYPT_HASH_AROUND"] = 10
    app.config["BCRYPT_HASH_PREFIX"] = "$2y$"
    app.config["BCRYPT_HASH_SALT_LENGTH"] = 22
    return app

