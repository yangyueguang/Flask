# coding: utf-8
# @date: 2019-11-10
import os
import sys


def full_url(host, port, url):
    real_host = os.getenv(host, 'localhost')
    real_port = os.getenv(port, '8000')
    return 'http://{}:{}{}'.format(real_host, real_port, url)


CURR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURR_PATH)
IS_DEBUG = True
LOG_PATH = os.path.join(CURR_PATH, 'logs')


