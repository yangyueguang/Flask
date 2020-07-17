# coding: utf-8
# @date: 2019-11-10
from flask import request, g
import os
import datetime
import json
import uuid
import traceback
from flask_restful import reqparse
from app import config
from app.services.baseResp import BaseResp
from app.utility.dlog import dlog
from app.utility.extract_pdf import extract_pdf


class PdfExtract(BaseResp):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('time', type=int, required=True, help='Params time Required!')
        file = request.files['file']
        if not file:
            raise ValueError('File is required')
        if not file.filename.lower().endswith('.pdf'):
            raise ValueError('Only support pdf file')
        file_path = 'data/static/' + file.filename
        file.save(file_path)
        file.close()
        extract_result = extract_pdf(file_path)
        args = parser.parse_args()
        time_str = args['time']
        print(time_str)
        return self.resp(data={'result': 'OK'})

