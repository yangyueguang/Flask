# coding: utf-8
# @date: 2019-11-10
from flask import request
import os
import datetime
import json
import traceback
from flask_restful import reqparse
from app import config
from app.services.baseResp import BaseResp
from app.utility.dlog import dlog


class PdfExtract(BaseResp):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('time', type=int, required=True, help='Params time Required!')
        args = parser.parse_args()
        try:
            time_str = args['time']
            with open(os.path.join(config.CURR_PATH, 'data/time_report_interval.txt'), 'w') as f:
                f.write(str(time_str))
            return self.resp(data={'result': 'OK'})
        except Exception as e:
            dlog(traceback.format_exc(), True)
            return self.resp(code=500, message='服务器内部错误', data=None)

