# coding: utf-8
# @date: 2019-11-10
from functools import partial
from flask import request
from flask import jsonify
from flask_restful import Resource
from app.utility.dlog import dlog


class BaseResp(Resource):

    def resp(self, code=200, message='Success', data=''):
        dlog(request.path)
        dlog(request.args)
        dlog(request.form)
        dlog({'response': data})
        return {'code': code, 'message': message, 'data': data}

    def abort(self, message, code=200):
        dlog('abort:' + message, True)
        return self.resp(code=code, message=message), code
