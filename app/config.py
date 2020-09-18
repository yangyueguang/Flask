# coding: utf-8
# @date: 2019-11-10
import os
import sys

import multiprocessing

bind = '0.0.0.0:8000'
workers = os.environ.get('WORKERS', multiprocessing.cpu_count())
threads = os.environ.get('THREADS', 1 if multiprocessing.cpu_count() == 1 else 2)
CURR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURR_PATH)
IS_DEBUG = True
# 如果部署的时候开启了debug模式, 可以启用auto_reload
reload = True

LOG_PATH = os.path.join(CURR_PATH, 'data/logs')
# redis conf
REDIS_CONF = {
    'host': os.getenv('REDIS_HOST', "127.0.0.1"),
    'port': os.getenv('REDIS_PORT', 6379),
    'db': os.getenv('REDIS_DB', 1),
    'password': os.getenv('REDIS_PASS', None)
}

ORACLE_CONF = {
    'host': '100.100.21.163',
    'port': '1521',
    'username': 'system',
    'password': 'oracle',
    'service': 'xe',
}

