# coding: utf-8
from apps import config


class StatusType(enumerate):
    ok = 'OK'
    warn = 'WARN'
    error = 'ERROR'


# 上报数据对象
class Report(object):
    def __init__(self):
        self.status = {}
        self.statistics = {}
        self.message = {}

    def tojson(self):
        return {
            "status":self.status,
            "statistics":self.statistics,
            "messages": self.message
        }

    @staticmethod
    def get_config():
        api_config = {
            'idps': config.URL_IDPS,
            'ocr': config.URL_OCR,
            'search': config.URL_SEARCH,
            'merge': config.URL_MERGE,
            'nlp': {
                'tongji': config.URL_TONGJI,
                'text_process': config.URL_TEXT_PROCESS,
                'preprocess': config.URL_PREPROCESS,
                'tagging': config.URL_TAGGING,
                'summary': config.URL_SUMMARY,
                'knowledge': config.URL_KNOWLEDGE
            }
        }
        return api_config

