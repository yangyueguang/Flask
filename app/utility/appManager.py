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

import time
from flask.wrappers import Request as _Request

class NoAuthResponse(Exception):

    def __init__(self, msg):
        self.msg = msg

    def show(self):
        return self.msg



class Request(_Request):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.request_id = int(time.time())
        self._param = None

    @property
    def params(self):
        """
        根据不同类型的请求去获取对应的data
        POST, PUT -> request.data or request.form
        GET, DELETE -> request.args
        """
        if self._param is not None:
            return self._param

        data = {}
        if self.method in ("POST", "PUT"):
            data = self.get_json(force=True) if self.data.strip() else {k: v for k, v in self.form.items()}
        elif self.method in ("DELETE", "GET"):
            data = self.args
        self._param = data
        return data






def create_app():
    dlog('--start to run logs upload server--')
    flask_app = Flask(__name__, template_folder='data/static', static_folder="data/upload", static_url_path='/upload')
    # redis_db.connect_redis()
    load_conf(flask_app)
    flask_app.request_class = Request
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

    @flask_app.errorhandler(Exception)
    def base_handler(error):
        """
        @attention: 未知异常
        """
        return jsonify({'code': 500, 'message': ''}), 500

    @flask_app.errorhandler(NoAuthResponse)
    def no_auth_response(error: NoAuthResponse):
        return jsonify({'code': 500, 'message': ''}), 500

    @flask_app.before_request
    def jwt_auth():
        from flask_jwt_extended import verify_jwt_in_request
        from jwt.exceptions import ExpiredSignatureError
        try:
            verify_jwt_in_request()
        except ExpiredSignatureError:
            print('error')


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


def register_plugins(flask_app):

    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(dsn='dns', integrations=[FlaskIntegration()])
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
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 60*60*24  # token过期时间
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 30
    app.config["SSO_LOGIGN"] = True  # 是否支持单点登录 True:支持，False:不支持
    app.config["SECRET_KEY"] = "secret$%^&*key!@#$%^774ST$%^&*(you#!!@%never!@#$%^&guess"
    app.config["JWT_SECRET_KEY"] = "secret$%^&*key!@#$%^774@@$%^&*(you#!!@%never!@#$%^&guess"

    app.config["BCRYPT_HASH_AROUND"] = 10
    app.config["BCRYPT_HASH_PREFIX"] = "$2y$"
    app.config["BCRYPT_HASH_SALT_LENGTH"] = 22
    return app

