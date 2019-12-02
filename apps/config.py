# coding: utf-8
# @date: 2019-11-10
# @author: xuechao@datagrand.com
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


URL_IDPS = full_url('IDPS_HOST', 'IDPS_PORT', '/extract')
URL_OCR = full_url('OCR_HOST', 'OCR_PORT', '/ocr')
URL_SEARCH = full_url('SEARCH_HOST', 'SEARCH_PORT', '/search/pangu')
URL_MERGE = full_url('MERGE_HOST', 'MERGE_PORT', '/api/report')
# 统计信息 es_ip和es_port 现在都是打洞到本地，ip是同一个ip，端口可以根据docker ps|grep nlp查看各个服务的端口
URL_TONGJI = full_url('NLP_HOST_TONGJI', 'NLP_PORT_TONGJI', '/pangu_zz57_1574241194/_search')
URL_TEXT_PROCESS = full_url('NLP_HOST_TEXT_PROCESS', 'NLP_PORT_TEXT_PROCESS', '/text_process/')
URL_PREPROCESS = full_url('NLP_HOST_PREPROCESS', 'NLP_PORT_PREPROCESS', '/preprocess/')
URL_TAGGING = full_url('NLP_HOST_TAGGING', 'NLP_PORT_TAGGING', '/tagging/?text=1')
URL_SUMMARY = full_url('NLP_HOST_SUMMARY', 'NLP_PORT_SUMMARY', '/summary/?text=1')
URL_KNOWLEDGE = full_url('NLP_HOST_KNOWLEDGE', 'NLP_PORT_KNOWLEDGE', '/knowledge/')

URL_IDPS_LOGIN = full_url('IDPS_LOGIN_HOST', 'IDPS_LOGIN_PORT', '')
IDPS_USERNAME = os.getenv('IDPS_USERNAME', 'superadminpro')
IDPS_PASSWORD = os.getenv('IDPS_PASSWORD', 'BEgPDsMumFlc')
RELOGIN_INTERVAL = int(os.getenv('RELOGIN_INTERVAL', '60'))
PROCESS_NUM = int(os.getenv('PROCESS_NUM', '1'))
SCAN_TIME_INTERVAL = int(os.getenv('SCAN_TIME_INTERVAL', '60'))


