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

        }
        return api_config

