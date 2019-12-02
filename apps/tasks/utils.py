# coding=utf-8
import os
import time
import json
from apps import config
import requests
from apps.utility.dlog import logger

LAST_LOGIN_TIME = None
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Authorization': None}


def auto_login(func):
    def wrapper(*args, **kwargs):
        global LAST_LOGIN_TIME
        if not LAST_LOGIN_TIME or (time.time() - LAST_LOGIN_TIME) >= config.RELOGIN_INTERVAL:
            logger.info('last login time expire: %s' % (time.ctime(LAST_LOGIN_TIME) if LAST_LOGIN_TIME else 'None'))
            login()
            LAST_LOGIN_TIME = time.time()
        return func(*args, **kwargs)
    return wrapper


def login():
    url = config.URL_IDPS_LOGIN + '/api/login'
    param_dict = {'username': config.IDPS_USERNAME, 'password': config.IDPS_PASSWORD}
    try:
        response_code, response = post(url, param_dict)
        if response_code >= 400:
            logger.error('IDPS登陆失败')
        if response:
            token = json.loads(response).get('access_token', '')
            HEADERS['Authorization'] = 'Bearer ' + token
            logger.info('IPDS login success. token: ' + token)
    except Exception as e:
        logger.error(e)


def post(url, param_dict, file='', param_type='x-www-form-urlencode'):
    '''
    @功能：封装post方式
    @paramType:指传入参数类型，可以是form-data、x-www-form-urlencode、json
    '''

    response_code = 500
    response = None
    try:
        if param_type == 'json':
            params = json.dumps(param_dict)
        else:
            params = param_dict
        if file == '':
            ret = requests.post(url, data=params, headers=HEADERS)
        else:
            files = {'file': open(file, 'rb')}
            ret = requests.post(url, data=params, headers=HEADERS, files=files)
        response_code = ret.status_code
        response = ret.text
    except:
        logger.error('login error')
    return response_code, response


def get(url, param_dict=None):
    response_code = 500
    response = None
    try:
        ret = requests.get(url, data=param_dict, headers=HEADERS)
        response_code = ret.status_code
        response = ret.text
    except Exception as e:
        logger.error(e)
    return response_code, response
