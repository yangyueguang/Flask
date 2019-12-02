# coding: utf-8
# @date: 2019-11-10
# @author: xuechao@datagrand.com
from functools import partial
from flask import request
from flask import jsonify
from flask_restful import Resource
from apps.utility.dlog import logger


class BaseResp(Resource):

    def resp(self, code=200, message='Success', data=''):
        logger.info(request.path)
        logger.info(request.args)
        logger.info(request.form)
        logger.info({'response': data})
        return {'code': code, 'message': message, 'data': data}

    def abort(self, message, code=200):
        logger.error('abort:' + message)
        return self.resp(code=code, message=message), code
