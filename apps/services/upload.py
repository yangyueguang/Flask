# coding: utf-8
# @date: 2019-11-10
# @author: xuechao@datagrand.com
from flask import request
import os
import datetime
import json
from flask_restful import reqparse
from apps import config
from apps.services.baseResp import BaseResp
from apps.utility.dlog import logger


class ChangeTimeInteval(BaseResp):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('time', type=int, required=True, help='Params time Required!')
        args = parser.parse_args()
        try:
            time_str = args['time']
            with open(os.path.join(config.CURR_PATH, 'static/time_report_interval.txt'), 'w') as f:
                f.write(str(time_str))
            return self.resp(data={'result': 'OK'})
        except Exception as e:
            logger.error(e)
            return self.resp(code=500, message='服务器内部错误', data=None)

