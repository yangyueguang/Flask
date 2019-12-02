# coding: utf-8
import os
import sys
import json
import datetime
import requests
from time import sleep
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(BASE_DIR)
sys.path.append(BASE_DIR)
from apps.utility.dlog import logger
from apps.tasks.sumLogs import *
from apps import config
from apps.tasks import utils
api = Report.get_config()
logger.info(api)
report = Report()


class LogHandler(object):
    def __init__(self):
        self.last_execute_time = datetime.datetime.min

    """获取上报时间间隔"""
    @property
    def time_interval(self):
        time_path = os.path.join(config.CURR_PATH, 'static/time_report_interval.txt')
        try:
            with open(time_path, 'r') as f:
                res = f.read()
                return int(res)
        except:
            return 5 * 60

    def run(self):
        scantime = config.SCAN_TIME_INTERVAL
        while True:
            time_interval = (datetime.datetime.now() - self.last_execute_time).seconds
            if time_interval >= self.time_interval:
                self.last_execute_time = datetime.datetime.now()
                self.execute_upload_task()
            sleep(scantime)

    """ 执行上报任务 """
    def execute_upload_task(self):
        report.statistics = {}
        try:
            self.request_ocr_logs()
            self.request_idps_logs()
            self.request_nlp_logs()
            self.request_search_logs()
            self.upload_logs()
        except Exception as e:
            logger.error(e)

    """ 拉取OCR的状态和统计信息 """
    def request_ocr_logs(self):
        try:
            res = requests.post(url=api['ocr'], files={'file': None}, timeout=10)
            if res.text == 'No file upload':
                status_code = StatusType.ok
                message = 'OK'
            else:
                status_code = StatusType.warn
                message = 'time out'
        except Exception as e:
            status_code = StatusType.error
            message = str(e)
            logger.error(e)
        report.status['ocr'] = status_code
        report.message['ocr'] = message

    @utils.auto_login
    def _idps_statistics(self):
        url = config.URL_IDPS_LOGIN + '/api/stats/label/total'
        response_code, response = utils.get(url)
        if response:
            return json.loads(response)
        else:
            return {}

    """ 拉取IDPS的状态和统计信息 """
    def request_idps_logs(self):
        params = {
            "content": "",
            "doc_type": 29,
            "rich_content": {}
        }
        status_code = StatusType.error
        message = 'error'
        try:
            res = requests.post(url=api['idps'], json=params, timeout=10)
            if res.status_code == 200 and res.json().get('status', '') == 'OK':
                status_code = StatusType.ok
                message = 'OK'
            else:
                status_code = StatusType.warn
                message = res.json().get('message', 'time out')
        except Exception as e:
            message = str(e)
            logger.error(e)
        report.status['idps'] = status_code
        report.message['idps'] = message
        counter = self._idps_statistics()
        report.statistics.update(counter)

    def _safe_request(self, method, url):
        try:
            res = requests.request(method, url, timeout=10)
            if res.status_code == 200 and ('"status": "OK"' in res.text or 'wrong method' in res.text):
                return StatusType.ok, 'OK'
            else:
                return StatusType.warn, '404: Not Found'
        except Exception as e:
            logger.error(e)
            return StatusType.error, str(e)

    """ 获取NLP的状态和统计信息 其中服务较多，都放在统计字段里了 """
    def request_nlp_logs(self):
        urls = api['nlp']
        params = {
            "size": 0,
            "aggs": {
                "count_classify": {
                    "cardinality": {
                        "field": "file_classify.keyword"
                    }
                },
                "count_tags": {
                    "cardinality": {
                        "field": "file_tags.keyword"
                    }
                },
                "count_keywords": {
                    "cardinality": {
                        "field": "file_keywords.keyword"
                    }
                }
            }
        }
        try:
            res = requests.get(urls['tongji'], json=params)
            res_json = res.json()
            if 'error' not in res_json.keys():
                aggregations = res_json.get('aggregations', {})
                classify_num = aggregations.get('count_classify', {}).get('value', 0)
                tags_num = aggregations.get('count_tags', {}).get('value', 0)
                keywords_num = aggregations.get('count_keywords', {}).get('value', 0)
                counter = {
                    "classify_num": classify_num,
                    "tags_num": tags_num,
                    "keywords_num": keywords_num
                }
                report.statistics.update(counter)
        except Exception as e:
            logger.error(e)

        tp_c, tp_m = self._safe_request('get', urls['text_process'])
        p_c, p_m = self._safe_request('get', urls['preprocess'])
        t_c, t_m = self._safe_request('post', urls['tagging'])
        s_c, s_m = self._safe_request('post', urls['summary'])
        k_c, k_m = self._safe_request('get', urls['knowledge'])

        report.status['text_process'] = tp_c
        report.message['text_process'] = tp_m
        report.status['preprocess'] = p_c
        report.message['preprocess'] = p_m
        report.status['tagging'] = t_c
        report.message['tagging'] = t_m
        report.status['summary'] = s_c
        report.message['summary'] = s_m
        report.status['knowledge'] = k_c
        report.message['knowledge'] = k_m

    """ 获取搜索的状态和统计信息 """
    def request_search_logs(self):
        try:
            res = requests.get(url=api['search'], timeout=10)
            if res.status_code == 200 and res.json().get('status', 1) == 0:
                status_code = StatusType.ok
                message = 'OK'
            else:
                status_code = StatusType.warn
                message = str(res.content)
        except Exception as e:
            logger.error(e)
            status_code = StatusType.error
            message = str(e)
        report.status['search'] = status_code
        report.message['search'] = message

    """ 上报数据 """
    def upload_logs(self):
        logger.info(report.tojson())
        try:
            requests.post(url=api['merge'], data=report.tojson())
        except Exception as e:
            logger.error(e)

    """ 格式化打印返回信息 """
    def dlog(self, data):
        jsonStr = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)
        print(jsonStr)


if __name__ == '__main__':
    logHand = LogHandler()
    logHand.run()
