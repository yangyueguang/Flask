# coding: utf-8
# @date: 2019-11-10

from flask_restful import Api
from apps.services import *

routes = {
    '/change_time_inteval': ChangeTimeInteval  # 修改循环时间
}


def add_routes(flask_app):
    api = Api(app=flask_app)
    for url, handler in routes.items():
        api.add_resource(handler, url)
