# coding: utf-8
# @date: 2019-11-10

from flask_restful import Api
from app.services import *

routes = {
    '/extract': PdfExtract
}


def add_routes(flask_app):
    api = Api(app=flask_app)
    for url, handler in routes.items():
        api.add_resource(handler, url)
